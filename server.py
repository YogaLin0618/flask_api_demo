from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger
from flask_socketio import SocketIO, emit
import os

load_dotenv()

template = {
  "swagger": "2.0",
  "info": {
    "title": "Jason's API Doc",
    "description": "API 文件描述",
    "version": "1.0.0"
  },
  "host": "localhost:443",  # overrides localhost:500
  "basePath": "",  # base bash for blueprint registration
  "schemes": [
    # "http",
    "https"
  ],
  "tags": [
      {
          "name": "User",
          "description": "系統中的使用者資訊"
      },
      {
          "name": "Account",
          "description": "系統中的帳戶資訊"
      }
  ]
}

app = Flask(__name__)

# 連接資料庫
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_STRING')
db = SQLAlchemy(app)
swagger = Swagger(app, template=template)

socketio = SocketIO(app)