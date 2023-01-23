# Learning Flask - Hello World

Against its name, this is not a "Hello World" app :smile:.

Instead, inside consecutively numbered folders you will find examples that would lead you from a simple "Hello World" app to more complex (and useful) ones.

## Setup

To create virtual environment run:

### _Linux_

```bash
python -m venv .venv
./.venv/Scripts/activate
```

### _Windows_

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

To start Flask application you need to change current directory to the one with `app.py` file and run (provided that you activated virtual environment):

```bash
python app.py
```

Alternatively, you can use `flask` command:

```bash
flask run
```

But first you need to set `FLASK_APP` environment variable:

```bash
export FLASK_APP=app.py
```

You can also set `FLASK_ENV` environment variable to `development` to enable debug mode (this variable is considered deprecated in favor of `FLASK_DEBUG`):

```bash
export FLASK_ENV=development
```

It is also possible to set `FLASK_DEBUG` environment variable to `1` to enable debug mode:

```bash
export FLASK_DEBUG=1
```

Under Windows we would use `set` command instead of `export`:

```cmd
set FLASK_APP=app.py
```

or PowerShell:

```powershell
$env:FLASK_APP = "app.py"
```

Side note: if you want list all versions of Python installed on your machine run (on Windows):

```cmd
py --list
```

To select specific version of Python run:

```cmd
py -3.8
```

## Learning Resources

This app is based on:

- _[Writing a Web Application with Flask](https://learning.oreilly.com/videos/writing-a-web/10000MNHV2021147/) [:file_folder:](https://github.com/writeson/manning_twitch_presentation)_.
