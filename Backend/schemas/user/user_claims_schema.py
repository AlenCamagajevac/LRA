from core.auth.user_claims import UserClaims
from marshmallow import Schema, fields, post_load
from schemas.auth.role_schema import RoleSchema


class UserClaimsSchema(Schema):
    email = fields.Email()

    roles = fields.Nested(RoleSchema, many=True)

    @post_load
    def create_user_claims(self, data, **kwargs):
        return UserClaims(**data)
