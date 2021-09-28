# 在 Python 中，包含 __init__.py 文件的子目录被视为一个包，可以导入。
from flask import Flask
from flask_cors import CORS
# 初始化app容器服务调用
app = Flask(__name__, static_folder='./static')
# 将返回的'\uXXXX'等编码为中文，在网页中显示
app.config['JSON_AS_ASCII'] = False
CORS(app)
# 调用服务的逻辑主代码
from app import demo