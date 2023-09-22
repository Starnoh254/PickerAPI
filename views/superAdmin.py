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