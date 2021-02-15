from rolepermissions.roles import AbstractUserRole


class AdminDeveloper(AbstractUserRole):
    available_permissions = {
    'edit' : True,
    'add' : True,
    'view' : True,
    'delete' : True,
    }



class EndUser(AbstractUserRole):
    available_permissions = {
    'edit' : False,
    'add' : False,
    'view' : True,
    'delete': False,
    }


