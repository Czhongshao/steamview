# 学习笔记

## 一、Flask

### Ⅰ：Flask 基础知识

#### 1. 路由（Routing）

路由是 URL 到 Python 函数的映射机制。它允许开发者定义特定的 URL 模式，并将其与对应的视图函数关联起来。当用户访问某个 URL 时，Flask 会根据路由规则调用相应的视图函数来处理请求。

~~~python
from flask import Flask

app = Flask(__name__)

# 将根 URL “/” 映射到 home 函数
@app.route('/')
def home():
    return 'Welcome to the Home Page!'

# 将 “/about” URL 映射到 about 函数
@app.route('/about')
def about():
    return 'This is the About Page.'
~~~

#### 2. 视图函数（View Functions）

视图函数是 Flask 中用于处理请求并返回响应的 Python 函数。它们通常接收请求对象作为参数，并返回响应对象，或者直接返回字符串、HTML 等内容。

~~~python
from flask import request

@app.route('/greet/<name>')
def greet(name):
    # greet 函数接收 URL 中的 name 参数，并返回一个字符串响应
    return f'Hello, {name}!'
~~~

#### 3. 请求对象（Request Object）

请求对象包含了客户端发送的请求信息，例如请求方法、URL、请求头、表单数据等。Flask 提供了 `request` 对象来方便开发者访问这些信息。

~~~python
from flask import request

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')  # 获取 POST 请求中表单数据的 username 字段
    return f'Hello, {username}!'
~~~

#### 4. 响应对象（Response Object）

响应对象包含了发送给客户端的响应信息，包括状态码、响应头和响应体。在 Flask 中，字符串、HTML 等内容可以直接作为响应体返回。如果需要创建更复杂的响应对象，可以使用 `make_response` 方法。

~~~python
from flask import make_response

@app.route('/custom_response')
def custom_response():
    response = make_response('This is a custom response!')  # 创建一个自定义响应对象
    response.headers['X-Custom-Header'] = 'Value'
    return response
~~~

#### 5. 模板（Templates）

Flask 使用 Jinja2 模板引擎来渲染 HTML 模板。模板允许开发者将 Python 代码嵌入到 HTML 中，从而实现动态生成网页内容。

~~~python
from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
~~~

其中，模板文件（templates/hello.html）：

~~~html
<!DOCTYPE html>
<html>
<head>
    <title>Hello</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
~~~

#### 6. 应用工厂（Application Factory）

应用工厂是一个 Python 函数，用于创建和配置 Flask 应用实例。通过应用工厂，开发者可以在不同的配置下初始化应用，或者创建多个应用实例。

~~~python
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
~~~

#### 7. 配置对象（Configuration Objects）

配置对象用于设置应用的各种配置选项，例如数据库连接字符串、调试模式等。开发者可以通过直接设置或加载配置文件来配置 Flask 应用。

~~~python
# app.config.from_object(Config)：将 Config 类中的配置项加载到应用配置中
class Config:
    DEBUG = True
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
~~~

#### 8. 蓝图（Blueprints）

蓝图是 Flask 中用于组织代码的一种方式。它允许开发者将相关的视图函数、模板和静态文件组织在一起，并且可以在多个应用中重用。

~~~python
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return 'Home Page'
~~~

注册蓝图（app/\_\_init\_\_.py）：

~~~python
from flask import Flask
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app
~~~

#### 9. 静态文件（Static Files）

静态文件是指不会被服务器端执行的文件，例如 CSS、JavaScript 和图片文件。Flask 提供了一个简单的方法来服务这些文件。

~~~python
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
~~~

将静态文件放在 `static` 文件夹中，Flask 会自动提供服务。

#### 10. 拓展（Extensions）

Flask 拥有许多扩展，可以为应用添加额外的功能，例如数据库集成、表单验证、用户认证等。这些扩展提供了更高级的功能和第三方集成。

~~~python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
~~~

SQLAlchemy 是一个用于数据库集成的扩展。

#### 11. 会话（Sessions）

Flask 使用客户端会话来存储用户信息，以便在用户浏览应用时记住他们的状态。会话数据存储在客户端的 cookie 中，并在服务器端进行签名和加密。

~~~python
from flask import session

# 自动生成的密钥
app.secret_key = 'your_secret_key_here'

@app.route('/set_session/<username>')
def set_session(username):
    session['username'] = username
    return f'Session set for {username}'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    return f'Hello, {username}!' if username else 'No session data'
~~~

**提示：** 可以使用 Python 内置的 `secrets` 模块生成一个强随机性的密钥。

~~~bash
python -c 'import secrets; print(secrets.token_hex())'
~~~

#### 12. 错误处理（Error Handling）

Flask 允许定义错误处理函数，当特定的错误发生时，这些函数会被调用。开发者可以自定义错误页面或处理逻辑。

~~~python
@app.errorhandler(404)
def page_not_found(e):
    return 'Page not found', 404

@app.errorhandler(500)
def internal_server_error(e):
    return 'Internal server error', 500
~~~

`@app.errorhandler(404)` 定义了 404 错误的处理函数，返回自定义的错误页面。

___

### Ⅱ：Flask 结构

#### 1. 简单项目结构

~~~cmd
flask_easy/
│
├── app.py
└── requirements.txt
~~~

- app.py: 主要的Flask应用文件，包含路由和视图函数的定义。

    ~~~python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello, World!'

    if __name__ == '__main__':
        app.run(debug=True)
    ~~~

- requirements.txt: 列出项目的依赖库，用于记录 Flask 和其他版本包的版本信息

#### 2. 中型项目结构

~~~cmd
flask_middle/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
│
├── config.py
├── requirements.txt
└── run.py
~~~

- app/: 包含Flask应用的主要代码
  - \_\_init\_\_.py: 初始化 Flask 应用和配置扩展。

    ~~~python
    from flask import Flask

    def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from . import routes
    app.register_blueprint(routes.bp)

    return app
    ~~~

  - routes.py: 定义应用的路由和视图函数

    ~~~python
    from flask import Blueprint

    bp = Blueprint('main', __name__)

    @bp.route('/')
    def home():
        return 'Hello, World!'
    ~~~

  - models.py: 定义应用的数据模型

- config.py: 配置文件, 包含应用的配置信息

- requirements.txt: 列出项目的依赖库

- run.py: 用于启动 Flask 应用

    ~~~python
    from app import create_app

    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)
    ~~~

#### 3. 复杂项目结构

~~~cmd
flask_complex/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── auth.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── templates/
│   │   ├── layout.html
│   │   └── home.html
│   └── static/
│       ├── css/
│       └── js/
│
├── config.py
├── requirements.txt
├── migrations/
│   └── ...
└── run.py
~~~

- app/routes/: 将不同功能的模块的路由分开管理
  - main.py: 主模块的路由

    ~~~python
    from flask import Blueprint, render_template

    bp = Blueprint('main', __name__)

    @bp.route('/')
    def home():
        return render_template('home.html')
    ~~~

  - auth.py: 认证相关的路由
- app/models/: 管理数据模型, 通常与数据库操作相关

    ~~~ python
    # app/models/user.py
    from app import db

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), unique=True, nullable=False)
    ~~~

- app/templates/: 存放 HTML 模板文件
- app/static/: 存放静态文件, Css和JavaScript等
- migrations/: 数据库迁移文件, 通常与 SQLAlchemy 相关

## 二、Vue

### Ⅰ：Vue 基础知识

#### 1. vue
