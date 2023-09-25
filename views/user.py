from flask_restful import Resource
from flask import request  
import pymysql

from functions import *

# I have imported only the necessary modules 

class PickerSignUp(Resource):
    def post(self):
        # Extract json data from the HTTP request and assign it to the variable json
        json = request.json
        # file = request.files['file']
        # file.save("static/ImageAssets/" + file.filename)


        driverID = generate_ids()

        firstName = json['firstName']
        lastName = json['lastName']
        county = json['county']
        constituency = json['constituency']
        mobileNumber = json['mobileNumber']
        email = json['email']
        idNumb = json['idNumb']
        address = json['address']
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
        INSERT INTO tbldriver
        (`DriverID`  , `First Name` ,`Last Name`, `County` , `Constituency` , `MobileNumber` , `Email` , 
        `Idnumb` , `Address` , `Password`) 
        VALUES (%s , %s , %s , %s , %s , %s , %s , %s , %s , %s )
          '''
        
        # Provide the data 
        data = (driverID  , firstName , lastName , county , constituency 
                , mobileNumber , email , idNumb , address , hash_password(password))

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


class PickerLogin(Resource):
    def post(self):

        json = request.json
        email = json['email']
        password = json['password']

        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = "garbagemsdb"

        )

        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = '''
SELECT * FROM tbldriver WHERE Email=%s ;
'''

        data = (email)

        try:

            cursor.execute(sql , data)
            count = cursor.rowcount
            if count == 0:
                response3= {'message':'Email Not Found'}
                return response3 ,  500
            else :
                result_set = cursor.fetchone()

                result_set["JoiningDate"] = str(result_set["JoiningDate"])

                # Return the modified result_set as a JSON response
                return {'message': result_set}

        except Exception as error:
            print(str(error))


class PickerPayment(Resource):
    def post(self):
        json = request.json
        phone = json['phone']
        amount = json['amount']

        try: 
            response = mpesa_payment(amount , phone)
            print(response)
            return response 
        except Exception as e:
            print(str(e))


class UpdateDetails(Resource):
    def post(self):
        json = request.json
        driverId = json['driverId']
        county = json['county']
        constituency = json['constituency']
        mobileNumber = json['mobileNumber']
        email = json['email']
        address = json['address']
        password = json['password']
     


        # create a database connection 

        
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = "garbagemsdb"

        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = '''UPDATE tbldriver 
        SET County = %s,Constituency = %s , MobileNumber = %s ,
          Email = %s , Address = %s , Password = %s
          WHERE ID = %s
          '''
        value = (county, constituency , mobileNumber, email , address, password, driverId)

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


class CheckNotification(Resource):
    def get(self):
        sql = 'SELECT * FROM tblnotifications'
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = "garbagemsdb"

        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
            count = cursor.rowcount
            if count == 0:
                return {'message ': "No notifications"}
            else:
                notifications = cursor.fetchall()
                for notification in notifications:
                    notification['time'] = str(notification['time'])
                    
                return notifications
        except Exception as e:
            print(str(e))


        