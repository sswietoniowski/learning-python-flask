# Learning Flask

Based on this course: _[Flask: Getting Started](https://app.pluralsight.com/library/courses/flask-getting-started/table-of-contents)_.

To create virtual environment run:

_Linux_

```
python -m venv venv
./venv/Scripts/activate
```

_Windows_

```
python -m venv venv
.\venv\Scripts\activate
```

To save requirements run:
```
pip freeze > requirements.txt
```

To install requirements run:

```
pip install -r requirements.txt
```

To start Flask application do this:

_Linux_

```
export FLASK_APP=flashcards.py
export FLASK_ENV=development
flask run
```

_Windows_ (Command Line)

```
set FLASK_APP=flashcards.py
set FLASK_ENV=development
flask run
```

_Windows_ (PowerShell)

```
$Env:FLASK_APP='flashcards.py'
$Env:FLASK_ENV='development'
flask run
```