from rolepermissions.roles import AbstractUserRole

class DepartmentChair(AbstractUserRole):
    available_permissions = {
        'view_department_class_rosters': True,
    }

class AOC(AbstractUserRole):
    available_permissions={
        'view_department_class_rosters': True,
    }

class GTA(AbstractUserRole):
    available_permissions = {
        'view_own_class_rosters': False
    }
