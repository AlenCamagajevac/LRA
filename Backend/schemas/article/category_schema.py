from marshmallow import Schema, fields


class CategorySchema(Schema):
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(dump_only=True)
