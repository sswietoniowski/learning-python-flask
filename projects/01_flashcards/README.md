# Flashcards

Based on this course: _[Flask: Getting Started](https://app.pluralsight.com/library/courses/flask-getting-started/table-of-contents)_.

Start page:

![Start page](./img/flashcards_01.JPG)

Viewing flashcard:

![Viewing flashcard](./img/flashcards_02.JPG)

Removing flashcard:

![Removing flashcard](./img/flashcards_03.JPG)

## Setup

To create virtual environment run:

_Linux_

```
python -m venv .venv
./venv/Scripts/activate
```

_Windows_

```
python -m venv .venv
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

If you don't want to use `flask run` you can use `python flashcards.py` instead.

One word about database (aka "flashcards_db.json"), provided that you don't want to commit changes to it. You can use `git update-index --assume-unchanged flashcards_db.json` to tell git to ignore changes to this file.

## Learning Resources

This app is based on:

- _[Flask: Getting Started](https://app.pluralsight.com/library/courses/flask-getting-started/table-of-contents)_ [:file_folder:](https://app.pluralsight.com/library/courses/flask-getting-started/exercise-files).
