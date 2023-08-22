from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# 連接資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/api'
db = SQLAlchemy(app)