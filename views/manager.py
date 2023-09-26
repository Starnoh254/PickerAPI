from flask_restful import Resource
from flask import request 
import pymysql
from functions import *

class ManagerLogin(Resource):
    def post(self):
        json = request.json
        password = json['password']
        email = json['email']

        sql = 'SELECT * FROM tbluser WHERE Email = %s'
        data = (email)

        # Create a connection to the database 
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        
        cursor = connection.cursor(cursor.DictCursor)

        try:
            cursor.execute(sql , data)
            connection.commit()
            count = cursor.rowcount
            if count == 0:
                return {'message ': 'Invalid email'}
            else:
                member = cursor.fetchone()
                hashedPassword = member['Password']
                if hash_verify(password , hashedPassword):

                    return {'message':'Login Successful'}
                else:
                    return {'message':'Login Failed , invalid password'}
                
        except Exception as error : 
            print(str(error))

        