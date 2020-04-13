from marshmallow import Schema, fields
from schemas.user.user_schema import UserSchema


class PaginatedUserSchema(Schema):
    has_next = fields.Boolean(dump_only=True)
    has_prev = fields.Boolean(dump_only=True)
    page = fields.Integer(dump_only=True)
    pages = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)
    items = fields.Nested(UserSchema, many=True, dump_only=True)
