from typing import List
from core.enum.role_enum import RoleTypes


class UserClaims():
    def __init__(self, email="", roles=[]):
        self.email = email
        self.roles = roles

    def is_admin(self):
        # Check if there is admin role in roles
        return True if next((
            (role for role in self.roles
             if role.role_type == RoleTypes.ADMIN)
        ), None) else False

    def is_client(self):
        # Check if there is client role in roles
        return True if next((
            (role for role in self.roles
             if role.role_type == RoleTypes.CLIENT)
        ), None) else False

    def contains_role(self, required_role: RoleTypes):
        return True if next((
            (role for role in self.roles
             if role.role_type == required_role)
        ), None) else False

    def contains_any_roles(self, required_roles: List[RoleTypes]):
        return True if next((
            (role for role in self.roles
             if role.role_type in required_roles)
        ), None) else False
