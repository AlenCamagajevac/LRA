from marshmallow import Schema, fields


class TokenSchema(Schema):
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
