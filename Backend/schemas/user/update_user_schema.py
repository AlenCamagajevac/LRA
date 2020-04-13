from marshmallow import Schema, fields, validate


class UpdateUserSchema(Schema):
    name = fields.Str(
        required=False,
        validate=validate.Length(min=3, max=100),
        load_only=True
    )
