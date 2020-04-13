from marshmallow import Schema, fields
from schemas.article.category_schema import CategorySchema
from schemas.user.user_details_schema import UserDetailsSchema


class ArticlePreviewSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    title = fields.Str(dump_only=True)
    preview = fields.Str(dump_only=True)
    category = fields.Nested(CategorySchema, many=False, dump_only=True)
    user = fields.Nested(UserDetailsSchema, many=False, dump_only=True)
    created_date = fields.DateTime(dump_only=True)
    last_update = fields.DateTime(dump_only=True)


class PaginatedArticleSchema(Schema):
    has_next = fields.Boolean(dump_only=True)
    has_prev = fields.Boolean(dump_only=True)
    page = fields.Integer(dump_only=True)
    pages = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)
    items = fields.Nested(ArticlePreviewSchema, many=True, dump_only=True)
