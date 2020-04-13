from marshmallow import Schema, fields


class ErrorResponseSchema(Schema):
    details = fields.Dict()
    error = fields.Str()
