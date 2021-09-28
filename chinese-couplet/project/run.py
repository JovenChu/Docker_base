#!flask/bin/python
from app import app
app.run(debug = True, host='0.0.0.0')
# Flask 应用程序实例的运行脚本，调用应用实例app中的__init__.py的程序
