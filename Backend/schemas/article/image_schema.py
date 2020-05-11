from marshmallow import Schema, fields


class ImageSchema(Schema):
    storage_id = fields.UUID(dump_only=True)
    is_cover = fields.Boolean(dump_only=True)