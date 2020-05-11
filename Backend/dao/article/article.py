from sqlalchemy.sql import func
from sqlalchemy.orm import column_property
from dao.base.base_model import BaseModel
from db import db
from core.enum.order_enum import OrderType


class Article(BaseModel):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    preview = column_property(func.substring(content, 0, 89) + '...')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # One article has many images
    images = db.relationship(
        'Image', lazy='subquery', backref=db.backref(
            'article', lazy='joined')
    )

    def __repr__(self):
        return '<Article %r>' % self.title

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def find_all_articles(cls, filter_params):
        query = cls.query

        query = query.filter(cls.title.like(f'%{filter_params["query"]}%'))

        if filter_params['from']:
            query = query.filter(cls.created_date >= filter_params['from'])

        if filter_params['to']:
            query = query.filter(cls.created_date <= filter_params['to'])

        if filter_params['sort'] == OrderType.ASCENDING:
            query = query.order_by(cls.created_date.asc())
        elif filter_params['sort'] == OrderType.DESCENDING:
            query = query.order_by(cls.created_date.desc())

        return query.paginate(
            filter_params['page'], filter_params['per_page'], error_out=False)

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
