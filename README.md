# flask-seek
Automatically discover and register  Blueprint and decorators (such as before_request), make the code more elegant .

## Requirements

- Python 3.6+
- Flask 1.1.0+

## Installation

```shell
$ pip install flask-seek
```

## A Simple Example

- Project structure and content

```shell
project
    hello.py
    main.py
```

```python
# main.py
from flask import Flask
from flask_seek import seek

app = Flask(__name__)


seek(app, blueprint_modules=["hello"])

if __name__ == "__main__":
    app.run()
```

```python
# hello.py
from flask import Blueprint

hello_bp = Blueprint("hello", __name__)


@hello_bp.route("/")
def hello():
    return {"msg": "Hello"}
```

- start

```
$ python main.py
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

```shell
$ curl -s http://127.0.0.1:5000/
{"msg":"Hello"}
```

## Example upgrade

```python
project
	common
        __init__.py
        error_handler.py
        middleware.py
	controller
        __init__.py
        hello.py
	main.py
```

```python
# main.py
from flask import Flask
from flask_seek import seek

app = Flask(__name__)


seek(app, blueprint_deep_modules=["controller"], decorator_modules=["common"])

if __name__ == "__main__":
    app.run()
```

```python
# hello.py
from flask import Blueprint

hello_bp = Blueprint("hello", __name__)


@hello_bp.route("/")
def hello():
    print("hello")
    return {"msg": "Hello"}

@hello_bp.route("/error")
def error():
    a = 1 / 0
    return {"msg": "Hello"}
```

```python
# error_handler.py
from flask_seek import ff


@ff.errorhandler(Exception)
def err(e):
    return {"msg": "Server Error"}
```

```python
# middlerware.py
from flask_seek import df


@df.before_request
def before():
    print("before_request")


@df.after_request
def after(resp):
    print("after_request")
    return resp
```

- start

```shell
$ python main.py
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

- Blueprint registered automatically

```shell
$ curl -s http://127.0.0.1:5000/
{"msg":"Hello"}
```

- before_request, after_request take effect

```shell
$ python main.py 
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
before_request
hello
after_request
127.0.0.1 - - [11/Jun/2021 00:06:13] "GET / HTTP/1.1" 200 -
```

- errorhandler take effect

```shell
$ curl -s http://127.0.0.1:5000/error
{"msg":"Server Error"}
```

## Guide

### seek

- parameters

  - instance - flask or buleprint instance 

  - blueprint_modules - List of blueprint modules path  such as `["common", "common.demo"]`

  - blueprint_deep_modules - It will recursively query all blueprint modules of the package

  - decorator_modules - List of flask decorator modules path

  - decorator_deep_modules - It will recursively query all decorator modules of the package

- example

```
project
	common
        __init__.py
        error_handler.py
        middleware.py
        demo
        	__init__.py
        	a.py   	
	main.py
```

```python
# main.py
from flask import Flask
from flask_seek import seek

app = Flask(__name__)


seek(app, decorator_modules=["common"]) # will search error_handler.py, middleware.py
seek(app, decorator_modules=["common.middleware"]) # will search middleware.py
seek(app, decorator_deep_modules=["common"]) # will search error_handler.py, middleware.py, a.py
seek(app, decorator_modules=["common.demo"]) # will search a.py
```

### df

decorator without parameters

```python
from flask_seek import df


@df.before_request
def before():
    print("before_request")
```

### ff

decorator with parameters

```python
from flask_seek import ff


@ff.errorhandler(Exception)
def err(e):
    return {"msg": "Server Error"}
```

## License

This project is licensed under the terms of the MIT license.







