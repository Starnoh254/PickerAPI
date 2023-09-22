from flask import Flask
from flask_restful import  Api



app = Flask(__name__)
api = Api(app)

from views.superAdmin import ManagerSignUp
from views.user import PickerSignUp , PickerLogin

# configure urls for user 
api.add_resource(PickerSignUp , '/api/signup_new_picker')
api.add_resource(PickerLogin , '/api/picker_login')

# configure urls for manager


# configure urls for super Admin
api.add_resource(ManagerSignUp , '/api/signup_new_manager')


if __name__ == '__main__':
    app.run(debug=True , port = 4000)
