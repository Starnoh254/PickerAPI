from flask import Flask
from flask_restful import  Api



app = Flask(__name__)
api = Api(app)

from views.superAdmin import ManagerSignUp , SuperAdminLogin , SendNotificationsToPickers , UpdateSuperAdminDetails
from views.superAdmin import ViewAllManagers , RemoveManager , ViewWastePickers , SendNotificationsToManagers
from views.user import PickerSignUp , PickerLogin , PickerPayment , UpdateDetails , CheckNotification

# configure urls for user 
api.add_resource(PickerSignUp , '/api/signup_new_picker')
api.add_resource(PickerLogin , '/api/picker_login')
api.add_resource(PickerPayment  , '/api/making_contributions')
api.add_resource(UpdateDetails , '/api/update_profile')
api.add_resource(CheckNotification , '/api/check_notification')
api.add_resource(SendNotificationsToPickers , '/api/send_notifications_to_pickers')
api.add_resource(SendNotificationsToManagers , '/api/send_notifications_to_managers')


# configure urls for manager


# configure urls for super Admin
api.add_resource(ManagerSignUp , '/api/signup_new_manager')
api.add_resource(SuperAdminLogin , '/api/super_admin_login')
api.add_resource(ViewAllManagers , '/api/view_managers')
api.add_resource(RemoveManager , '/api/remove_manager')
api.add_resource(ViewWastePickers , '/api/view_waste_pickers')
api.add_resource(UpdateSuperAdminDetails,'/api/update_super_admin_details')

if __name__ == '__main__':
    app.run(debug=True , port = 4000)
