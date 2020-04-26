from marshmallow import Schema, fields, post_load, validate, ValidationError
from dao.article.article import Article
from dao.article.category import Category


class CreateArticleSchema(Schema):
    title = fields.Str(
        required=True, validate=validate.Length(min=3, max=200))
    content = fields.Str(
        required=True, validate=validate.Length(min=3, max=10_000))
    category_id = fields.Integer(required=True)

    @post_load
    def make_article(self, data, **kwargs):
        # check if category exists
        category = Category.find_by_id(data['category_id'])
        if not category:
            raise ValidationError('Category with given uuid does not exist')
        del data['category_id']

        article = Article(**data)
        article.category = category

        return article
