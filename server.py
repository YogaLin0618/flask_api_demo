from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# 連接資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_STRING')
db = SQLAlchemy(app)