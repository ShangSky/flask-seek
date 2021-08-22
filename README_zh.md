# flask-seek

- [English](README.md)

使代码更优雅的flask扩展.

自动发现并注册蓝图和flask装饰器(例如before_request).

## 依赖

- Python 3.6+
- Flask 1.1.0+

## 安装

```shell
$ pip install flask-seek
```

## 简单的例子

- 项目结构和内容

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

- 运行

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

## 示例

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

- 运行

```shell
$ python main.py
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

- 自动注册蓝图

```shell
$ curl -s http://127.0.0.1:5000/
{"msg":"Hello"}
```

- before_request, after_request装饰器生效

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

- errorhandler装饰器生效

```shell
$ curl -s http://127.0.0.1:5000/error
{"msg":"Server Error"}
```

## 指引

### seek

- 参数

  - instance - Flask和Blueprint的实例

  - blueprint_modules - 蓝图模块路径列表, 例如 `["common", "common.demo"]`

  - blueprint_deep_modules - 递归查找的蓝图模块路径

  - decorator_modules - flask装饰器路径列表

  - decorator_deep_modules - 递归查找flask装饰器路径列表

- 示例

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


seek(app, decorator_modules=["common"]) # 会搜索到error_handler.py, middleware.py
seek(app, decorator_modules=["common.middleware"]) # 会搜索到middleware.py
seek(app, decorator_deep_modules=["common"]) # 会搜索到error_handler.py, middleware.py, a.py
seek(app, decorator_modules=["common.demo"]) # 会搜索到a.py
```

### df

装饰器

```python
from flask_seek import df


@df.before_request
def before():
    print("before_request")
```

### ff

带参装饰器

```python
from flask_seek import ff


@ff.errorhandler(Exception)
def err(e):
    return {"msg": "Server Error"}
```

## 许可证

此项目使用MIT许可证.
