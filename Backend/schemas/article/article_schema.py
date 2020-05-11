from marshmallow import Schema, fields, post_load
from dao.article.article import Article
from schemas.article.category_schema import CategorySchema
from schemas.user.user_details_schema import UserDetailsSchema
from schemas.article.image_schema import ImageSchema


class ArticleSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    title = fields.Str(dump_only=True)
    content = fields.Str(dump_only=True)
    category = fields.Nested(CategorySchema, many=False, dump_only=True)
    user = fields.Nested(UserDetailsSchema, many=False, dump_only=True)
    images = fields.Nested(ImageSchema, many=True, dump_only=True)
    created_date = fields.DateTime(dump_only=True)
    last_update = fields.DateTime(dump_only=True)

    @post_load
    def make_article(self, data, **kwargs):
        return Article(**data)
