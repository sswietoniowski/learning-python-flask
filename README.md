# Learning Flask

Based on this course: _[Flask: Getting Started](https://app.pluralsight.com/library/courses/flask-getting-started/table-of-contents)_.

To save requirements run:
```python
pip freeze > requirements.txt
```

To install requirements run:

```python
pip install -r requirements.txt
```

To start Flask application do this:

Linux:

```
export FLASK_APP=flashcards.py
export FLASK_ENV=development
flask run
```

Windows (Command Line):

```
set FLASK_APP=flashcards.py
set FLASK_ENV=development
flask run
```

Windows (PowerShell):

```
$Env:FLASK_APP='flashcards.py'
$Env:FLASK_ENV='development'
flask run
```