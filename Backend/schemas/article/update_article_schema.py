from marshmallow import Schema, fields, validate


class UpdateArticleSchema(Schema):
    title = fields.Str(
        required=False, validate=validate.Length(min=3, max=200))
    content = fields.Str(
        required=False, validate=validate.Length(min=3, max=10_000))
