from flask import Flask

app = Flask(__name__)


@app.route('/')  # 根url 路径
def index_page():  # 当用户访问根url 后，返回的内容
    return 'This is a index page.'


if __name__ == '__main__':
    app.run(debug=True)
