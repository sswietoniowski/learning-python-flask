from flask import (Flask, send_from_directory, render_template, request,
                   redirect, url_for, g, flash, jsonify)
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileAllowed, FileRequired
from markupsafe import Markup
from wtforms import (StringField, TextAreaField, SubmitField,
                     SelectField, DecimalField, FileField, HiddenField)
from wtforms.validators import InputRequired, DataRequired, Length, ValidationError
from wtforms.widgets import Input
from werkzeug.utils import secure_filename, escape, unescape
import sqlite3
from dotenv import load_dotenv
from livereload import Server
import os
from os.path import exists
import datetime
from secrets import token_hex


basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["jpeg", "jpg", "png"]
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["IMAGE_UPLOADS"] = os.path.join(basedir, "uploads")

app.config["TESTING"] = True

app.config["RECAPTCHA_PUBLIC_KEY"] = "NOT_REAL_PUBLIC_KEY"
app.config["RECAPTCHA_PRIVATE_KEY"] = "NOT_REAL_PRIVATE_KEY"


class PriceInput(Input):
    input_type = "number"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("step", "0.01")
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return Markup("""
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">$</span>
                </div>
                <input %s>
            </div>""" % self.html_params(name=field.name, **kwargs))


class PriceField(DecimalField):
    widget = PriceInput()


class ItemForm(FlaskForm):
    title = StringField("Title",
                        validators=[InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=5, max=20,
                                           message="Input must be between 5 and 20 characters long.")])

    price = PriceField("Price")
    description = TextAreaField("Description",
                                validators=[InputRequired("Input is required!"),
                                            DataRequired("Data is required!"),
                                            Length(min=5, max=40,
                                                   message="Input must be between 5 and 20 characters long.")])
    image = FileField("Image",
                      validators=[FileAllowed(app.config["ALLOWED_IMAGE_EXTENSIONS"], "Images only!")])


class BelongsToOtherFieldOption:
    def __init__(self, table, belongs_to, foreign_key=None, message=None):
        if not table:
            raise AttributeError("""
                BelongsToOtherFieldOption validator needs the table parameter.
            """)
        if not belongs_to:
            raise AttributeError("""
                BelongsToOtherFieldOption validator needs the belongs_to parameter.
            """)

        self.table = table
        self.belongs_to = belongs_to

        if not foreign_key:
            foreign_key = belongs_to + "_id"
        if not message:
            message = "Choosen option is not valid."
        else:
            self.message = message
            self.foreign_key = foreign_key

    def __call__(self, form, field):
        conn = get_db()
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT COUNT(*) FROM {self.table} AS t WHERE t.id = ? AND t.{self.foreign_key} = ?
            """, (field.data, getattr(form, self.belongs_to).data))
        except Exception as e:
            raise AttributeError("""
                Passed parameters are not correct. {}
            """.format(e))
        exists = c.fetchone()[0]
        if not exists:
            raise ValidationError(self.message)


class NewItemForm(ItemForm):
    category = SelectField("Category", coerce=int)
    subcategory = SelectField("Subcategory",
                              coerce=int,
                              validators=[BelongsToOtherFieldOption(
                                  table="subcategories",
                                  belongs_to="category",
                                  message="Subcategory does not belong to that category."
                              )])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")


class EditItemForm(ItemForm):
    submit = SubmitField("Update item")


class DeleteItemForm(FlaskForm):
    submit = SubmitField("Delete item")


class FilterForm(FlaskForm):
    title = StringField("Title", validators=[Length(max=20)])
    price = SelectField("Price", coerce=int, choices=[(0, '---'), (1, "Max to Min"), (2, "Min to Max")])
    category = SelectField("Category", coerce=int)
    subcategory = SelectField("Subcategory", coerce=int)
    submit = SubmitField("Filter")


class NewCommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[InputRequired("Input is required."),
                                                   DataRequired("Data is required.")])
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/category/<int:category_id>")
def category(category_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT s.id, s.name
        FROM subcategories AS s
        WHERE s.category_id = ?
    """, (category_id, ))
    subcategories = c.fetchall()

    return jsonify(subcategories=subcategories)


@app.route("/item/<int:item_id>")
def item(item_id):
    conn = get_db()
    c = conn.cursor()

    items_from_db = c.execute("""
        SELECT i.id, i.title, i.description, i.price, i.image, c.name, s.name
        FROM items AS i
        INNER JOIN categories AS c ON c.id = i.category_id
        INNER JOIN subcategories AS s ON s.id = i.subcategory_id
        WHERE i.id = ?
    """, (item_id, ))
    row = c.fetchone()

    try:
        item = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "image": row[4],
            "category": row[5],
            "subcategory": row[6]
        }
    except:
        item = {}

    if item:
        comments_from_db = c.execute("""
            SELECT c.content 
            FROM comments AS c
            WHERE c.item_id = ?
            ORDER BY c.id DESC            
        """, (item_id, ))
        comments = []
        for row in comments_from_db:
            comment = {
                "content": row[0]
            }
            comments.append(comment)

        new_comment_form = NewCommentForm()
        new_comment_form.item_id.data = item_id
        delete_item_form = DeleteItemForm()

        return render_template("item.html", item=item, delete_item_form=delete_item_form,
                               comments=comments, new_comment_form=new_comment_form)

    return redirect(url_for("home"))


@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    conn = get_db()
    c = conn.cursor()

    item_from_db = c.execute("""
        SELECT i.id, i.title, i.description, i.price, i.image 
        FROM items AS i
        WHERE i.id = ?
    """, (item_id,))
    row = c.fetchone()
    try:
        item = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "image": row[4]
        }
    except:
        item = {}

    if item:
        form = EditItemForm()
        if form.validate_on_submit():
            if form.image.data:
                filename = save_image_upload(form.image)
                if item.get("image") and exists(os.path.join(app.config["IMAGE_UPLOADS"], item["image"])):
                    os.remove(os.path.join(app.config["IMAGE_UPLOADS"], item["image"]))
            else:
                if item.get("image"):
                    filename = item.get("image")
                else:
                    filename = ""

            c.execute("""
                UPDATE items
                SET title = ?, description = ?, price = ?, image = ?
                WHERE id = ?
                """, (
                    escape(form.title.data),
                    escape(form.description.data),
                    float(escape(form.price.data)),
                    filename,
                    item_id
                )
            )
            conn.commit()

            flash(f"Item {item['title']} has been successfully updated.", "success")
            return redirect(url_for("item", item_id=item_id))

        form.title.data = unescape(item["title"])
        form.description.data = unescape(item["description"])
        form.price.data = item["price"]

        return render_template("edit_item.html", item=item, form=form)

    return redirect(url_for("home"))


@app.route("/item/<int:item_id>/delete", methods=["POST"])
def delete_item(item_id):
    conn = get_db()
    c = conn.cursor()

    item_from_db = c.execute("SELECT i.id, i.title, i.image FROM items AS i WHERE id = ?", (item_id, ))
    row = c.fetchone()

    try:
        item = {
            "id": row[0],
            "title": row[1],
            "image": row[2]
        }
    except:
        item = {}

    if item:
        if item.get("image") and exists(os.path.join(app.config["IMAGE_UPLOADS"], item["image"])):
            os.remove(os.path.join(app.config["IMAGE_UPLOADS"], item["image"]))
        c.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()

        flash(f"Item {item['title']} has been successfully deleted.", "success")
    else:
        flash("This item does not exist.", "danger")

    return redirect(url_for("home"))


@app.route("/comment/new", methods=["POST"])
def new_comment():
    conn = get_db()
    c = conn.cursor()
    form = NewCommentForm()

    try:
        is_ajax = int(request.form["ajax"])
    except:
        is_ajax = 0

    if form.validate_on_submit():
        c.execute("INSERT INTO comments (content, item_id) VALUES (?, ?)",
                  (escape(form.content.data), form.item_id.data))
        conn.commit()

        if is_ajax:
            return render_template("_comment.html", content=form.content.data)

    if is_ajax:
        return "Content is required.", 400

    return redirect(url_for("item", item_id=form.item_id.data))


@app.route("/")
def home():
    conn = get_db()
    c = conn.cursor()

    form = FilterForm(request.args, meta={"csrf": False})

    c.execute("SELECT id, name FROM categories AS c")
    categories = c.fetchall()
    categories.insert(0, (0, "---"))
    form.category.choices = categories

    c.execute("SELECT id, name FROM subcategories AS s")
    subcategories = c.fetchall()
    subcategories.insert(0, (0, "---"))
    form.subcategory.choices = subcategories

    query = """
        SELECT i.id, i.title, i.price, i.description, i.image, c.name, s.name
        FROM items AS i 
        INNER JOIN categories AS c on i.category_id = c.id
        INNER JOIN subcategories AS s ON i.subcategory_id = s.id    
    """

    try:
        is_ajax = int(request.args["ajax"])
    except:
        is_ajax = 0

    if form.validate():
        filter_queries = []
        parameters = []

        if form.title.data.strip():
            filter_queries.append("i.title LIKE ?")
            parameters.append("%" + escape(form.title.data) + "%")

        if form.category.data:
            filter_queries.append("i.category_id = ?")
            parameters.append(form.category.data)

        if form.subcategory.data:
            filter_queries.append("i.subcategory_id = ?")
            parameters.append(form.subcategory.data)

        if filter_queries:
            query += " WHERE "
            query += " AND ".join(filter_queries)

        if form.price.data:
            if form.price.data == 1:
                query += " ORDER BY i.price DESC"
            else:
                query += " ORDER BY i.price ASC"
        else:
            query += " ORDER BY i.id DESC"

        items_from_db = c.execute(query, tuple(parameters))
    else:
        items_from_db = c.execute(f"{query} ORDER BY i.id DESC")

    items = []
    for row in items_from_db:
        item = {
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "description": row[3],
            "image": row[4],
            "category": row[5],
            "subcategory": row[6]
        }
        items.append(item)

    if is_ajax:
        return render_template("_items.html", items=items)
    return render_template('home.html', items=items, form=form)


@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


def save_image_upload(image):
    format = "%Y%m%dT%H%M%S"
    now = datetime.datetime.utcnow().strftime(format)
    random_string = token_hex(2)
    filename = random_string + "_" + now + "_" + image.data.filename
    filename = secure_filename(filename)
    image.data.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
    return filename


@app.route("/item/new", methods=["GET", "POST"])
def new_item():
    conn = get_db()
    c = conn.cursor()
    form = NewItemForm()

    c.execute("SELECT id, name FROM categories")
    categories = c.fetchall()
    form.category.choices = categories

    c.execute("""SELECT id, name FROM subcategories""")
    subcategories = c.fetchall()
    form.subcategory.choices = subcategories

    if form.validate_on_submit() and form.image.validate(form, extra_validators=(FileRequired(),)):
        filename = save_image_upload(form.image)

        c.execute("""
            INSERT INTO items 
            (title, description, price, image, category_id, subcategory_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
            escape(form.title.data),
            escape(form.description.data),
            float(escape(form.price.data)),
            filename,
            form.category.data,
            form.subcategory.data
        )
                  )
        conn.commit()
        flash(f"Item {request.form.get('title')} has been successfully submitted.", "success")
        return redirect(url_for('home'))

    return render_template("new_item.html", form=form)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("db/globomantics.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def main():
    server = Server(app.wsgi_app)
    server.serve(debug=False)


if __name__ == '__main__':
    main()
