# Learning Flask - Hello World

Against its name, this is not a "Hello World" app :smile:.

Instead, inside consecutively numbered folders you will find examples that would lead you from a simple "Hello World" app to more complex (and useful) ones.

## Setup

To create virtual environment run:

_Linux_

```bash
python -m venv .venv
./.venv/Scripts/activate
```

_Windows_

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

To save requirements run:

```bash
pip freeze > requirements.txt
```

To install requirements run:

```bash
pip install -r requirements.txt
```

If you want to upgrade all packages to the latest version run:

```bash
pip install -r requirements.txt --upgrade
```

To start Flask application do this:

```bash
python app.py
```

## Learning Resources

This app is based on:

- _[Writing a Web Application with Flask](https://learning.oreilly.com/videos/writing-a-web/10000MNHV2021147/) [:file_folder:](https://github.com/writeson/manning_twitch_presentation)_.
