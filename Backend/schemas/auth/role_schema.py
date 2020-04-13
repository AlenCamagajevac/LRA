from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from core.enum.role_enum import RoleTypes
from dao.user.role import Role


class RoleSchema(Schema):
    role_type = EnumField(RoleTypes, by_value=True)
    description = fields.Str()

    @post_load
    def make_role(self, data, **kwargs):
        return Role(**data)
