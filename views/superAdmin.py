from flask_restful import Resource
from flask import request 
import pymysql
from functions import *

# I have imported only the necessary modules 

class ManagerSignUp(Resource):
    def post(self):
        # Extract json data from the HTTP request and assign it to the variable json
        json = request.json

        firstname = json['firstname']
        lastname = json['lastname']
        username = json['username']
        mobilenumber = json['mobilenumber']
        email = json['email']
        password = json['password']
        

        # Create a connection to the database 
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        
        cursor = connection.cursor()

        # Insert data into the database 
        sql = '''
        INSERT INTO tbluser
        (`First Name` , `Last Name` , `UserName` , `MobileNumber` , `Email` , `Password` )
        VALUES (%s , %s , %s , %s , %s , %s  )
          '''
        
        # Provide the data 
        data = (firstname , lastname , username , mobilenumber , email , hash_password(password ))

        try:
            cursor.execute(sql,data)
            connection.commit()

            response = {
                'Message': 'User Created Successfully'
            }
            return  response , 201
        except Exception as e: 
            connection.rollback()
            print(str(e))
            response2 = {
                'Message': 'User Creation Failed'
            }
            return response2 , 401
        
        finally:
            # Close the connection
            connection.close()

class SuperAdminLogin(Resource):
    def post(self):
        json = request.json
        userName = json['userName']
        password = json['password']

        sql = '''SELECT * FROM tbladmin WHERE UserName = %s '''
        # Create a connection to the database 
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        data = (userName)
        try:
            cursor.execute(sql,data)
            connection.commit()
            count = cursor.rowcount
            if count == 0:
                return {'message ': 'Invalid username'}
            else:
                member = cursor.fetchone()
                hashedPassword = member['Password']
                if hash_verify(password , hashedPassword):

                    return {'message':'Login Successful'}
                else:
                    return {'message':'Login Failed , invalid password'}
                
        except Exception as error : 
            print(str(error))

class ViewAllManagers(Resource):
    def get(self):
        sql = "SELECT * FROM tbluser"
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        count = cursor.rowcount
        if count == 0 :
            return {'message':"No managers found"}
        else:
            managers = cursor.fetchall()
            for manager in managers:
                manager['RegDate'] = str(manager['RegDate'])
            
            return managers
        
class RemoveManager(Resource):
    def delete(self):
        json = request.json
        id = json['id']

        sql = 'DELETE FROM tbluser WHERE ID = %s'
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        cursor = connection.cursor()
        data = (id)
        cursor.execute(sql,data)
        connection.commit()

        count = cursor.rowcount
        if count == 0:
            return {"message":"Record not deleted"}
        else:
            return{'message':'Record deleted successfully'}
        
class ViewWastePickers(Resource):
    def get(self):
        sql = 'SELECT * FROM tbldriver'
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        count = cursor.rowcount
        if count == 0 :
            return {'message':"No waste picker found"}
        else:
            pickers = cursor.fetchall()
            for picker in pickers:
                picker['JoiningDate'] = str(picker['JoiningDate'])
            
            return pickers
class SendNotificationsToPickers(Resource):
    def post(self):
        json = request.json
        notification = json['notification']
        sql = 'INSERT INTO tblnotifications (notifications) VALUES (%s)'
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        data = (notification)
        cursor = connection.cursor()
        count = cursor.execute(sql , data)
        connection.commit()
        if count == 0 :
            return {'message':'Failed to add Notifications'}
        else:
            return {'message':'Notification added successfully'}
        
class SendNotificationsToManagers(Resource):
    def post(self):
        json = request.json
        notification = json['notification']
        sql = 'INSERT INTO notifications_for_managers (notification) VALUES (%s)'
        connection =  pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "garbagemsdb"
                        )
        data = (notification)
        cursor = connection.cursor()
        count = cursor.execute(sql , data)
        connection.commit()
        if count == 0 :
            return {'message':'Failed to add Notifications'}
        else:
            return {'message':'Notification added successfully'}
        
class UpdateSuperAdminDetails(Resource):
    def post(self):
        json = request.json
        
        ID = json['id']
        mobileNumber = json['mobileNumber']
        email = json['email']
        username = json['username']
     


        # create a database connection 

        
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = "garbagemsdb"

        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = '''UPDATE tbladmin 
        SET UserName = %s,MobileNumber = %s ,
          Email = %s 
          WHERE ID = %s
          '''
        value = (username , mobileNumber, email , ID)

        try:
            cursor.execute(sql , value)
            connection.commit()
            count = cursor.rowcount
            if count == 0:
                return {'message ': "Error in Updating"}
            else:
                return {'message' : 'Profile successfully updated'}
        except Exception as error:
            print(str(error))





        
        