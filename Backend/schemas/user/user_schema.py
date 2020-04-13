from marshmallow import Schema, fields, post_load, validate, ValidationError
from schemas.auth.role_schema import RoleSchema
from dao.user.user import User


class UserSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    email = fields.Email(
        required=True, validate=validate.Length(min=3, max=100))
    roles = fields.Nested(RoleSchema, many=True, dump_only=True)
    password = fields.Str(required=False, validate=validate.Length(
        min=3, max=200), load_only=True)
    name = fields.Str(required=False, validate=validate.Length(min=3, max=200))
    allow_mail_notifications = fields.Boolean(required=False, dump_only=True)
    allow_push_notifications = fields.Boolean(required=False, dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        if not data['password']:
            raise ValidationError('Please provide password')

        password = data['password']
        del data['password']
        user = User(**data)
        user.set_password(password)

        return user
