from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
import pymysql
import traceback
from server import db
from models import UserModel

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

# 單筆 get
class User(Resource):
    
    # 串接 MySQL DB
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='password', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        return db, cursor
    
    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From api.users Where id = '{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()
        
        return jsonify({'data': user})
    
    def patch(self, id):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        # user = {
        #     'name': arg['name'],
        #     'gender': arg['gender'],
        #     'birth': arg['birth'],
        #     'note': arg['note']
        # }
        
        # query = []
        
        # for key, value in user.items():
        #     if value != None:
        #         query.append(key + ' = ' + "'{}'".format(value))
        
        # query = ", ".join(query)
        
        # sql = """
        #     UPDATE `api`.`users` SET {} WHERE (`id` = '{}');
        # """.format(query, id)
        
        user = UserModel.query.filter_by(id=id, deleted=None).first()
        if arg['name'] != None:
            user.name = arg['name']
        
        response = {}
        try:
            # cursor.execute(sql)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
            
        # db.commit()
        # db.close()
        
        return jsonify(response)
    
    # 硬刪除(不實用！真的刪除資料，要救回只能透過資料庫log紀錄)
    # def delete(self, id):
    #     db, cursor = self.db_init()
    #     sql = """
    #         DELETE FROM `api`.`users` WHERE (`id` = '{}');
    #     """.format(id)
        
    #     response = {}
    #     try:
    #         cursor.execute(sql)
    #         response['msg'] = 'success'
    #     except:
    #         traceback.print_exc()
    #         response['msg'] = 'failed'
            
    #     db.commit()
    #     db.close()
        
    #     return jsonify(response)

    # 軟刪除(較實用！)
    def delete(self, id):
        # db, cursor = self.db_init()
        # sql = """
        #     UPDATE `api`.`users` SET deleted = True WHERE (`id` = '{}');
        # """.format(id)
        
        response = {}
        try:
            # cursor.execute(sql)
            user = UserModel.query.filter_by(id=id, deleted=None).first()
            # db.session.delete(user) # 硬刪除！
            user.deleted = 1
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
            
        # db.commit()
        # db.close()
        
        return jsonify(response)
        

# 多筆 get, post
class Users(Resource):
    
    # 串接 MySQL DB
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='password', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        return db, cursor
    
    def get(self):
        # db, cursor = self.db_init()
        # gender = request.args.get('gender')
        # sql = 'Select * From api.users Where deleted is not True'
        # if gender != None:
        #     sql = sql + ' and gender = "{}"'.format(gender)
        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()
        
        # return jsonify({'data': users})
        
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})
    
    def post(self):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note']
        }
        # sql = """
        #     INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        # """.format(user['name'], user['gender'], user['birth'], user['note'])
        
        response = {}
        status_code = 200
        
        try:
            # cursor.execute(sql)
            new_user = UserModel(name=user['name'], gender=user['gender'], birth=user['birth'], note=user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'
            
        # db.commit()
        # db.close()
        
        return make_response(jsonify(response), status_code)