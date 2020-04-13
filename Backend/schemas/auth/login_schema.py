from core.dto.auth.login_dto import LoginDto
from marshmallow import Schema, fields, post_load, validate


class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    @post_load
    def make_login_dto(self, data, **kwargs):
        return LoginDto(**data)
