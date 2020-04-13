from marshmallow import Schema, fields, validate


class UserDetailsSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    email = fields.Email(
        required=True, validate=validate.Length(min=3, max=100))
    name = fields.Str(required=False, validate=validate.Length(min=3, max=200))
