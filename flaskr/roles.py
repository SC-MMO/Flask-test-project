import json
from .models import Role

def check_roles():
    with open('./flaskr/static/roles.json', 'r+') as roles_file:
        json_roles = json.load(roles_file)

        with open('./flaskr/static/permissions.json', 'r') as permissions_file:
            json_permissions = json.load(permissions_file)

        for json_role in json_roles.values():
            role_permissions = json_role.get("permissions", {})

            # Remove invalid permissions
            to_del = [perm for perm in role_permissions if perm not in json_permissions.keys()]
            for perm in to_del:
                del role_permissions[perm]

            # Add missing permissions with default value
            for perm in json_permissions.keys():
                if perm not in role_permissions:
                    role_permissions[perm] = json_permissions.get(perm)

            json_role['permissions'] = role_permissions

        # Got ot the beginning of the file and delete the old file content
        roles_file.seek(0)
        roles_file.truncate()

        json.dump(json_roles, roles_file, indent=4)
                    
                    
def add_db_roles():
    with open('./flaskr/static/roles.json', 'r') as roles_file:
        json_roles = json.load(roles_file)

    for role_name, role_data in json_roles.items():
        permissions = role_data.get("permissions", {})
        role = Role.objects(name=role_name).first()

        if not role:
            # Create new role if it doesn't exist
            role = Role(name=role_name, permissions=permissions)
        elif role.permissions != permissions:
            # Update permissions if they differ
            role.permissions = permissions

        role.save()
 
def init_roles():
    check_roles()
    add_db_roles()
