# 資料庫樣貌
from server import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    gender = db.Column(db.Integer)
    birth = db.Column(db.DATETIME)
    note = db.Column(db.Text)
    deleted = db.Column(db.Boolean)
    
    def __init__(self, name, gender, birth, note, deleted = None):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.note = note
        self.deleted = deleted
        
    # 回傳 dict 結構
    def serialize(self):
        return{
            "name": self.name,
            "gender": self.gender,
            "birth": self.birth,
            "note": self.note,
            "deleted": self.deleted
        }