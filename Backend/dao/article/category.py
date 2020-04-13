from dao.base.base_model import BaseModel
from db import db


class Category(BaseModel):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    # 1 to N relationship with articles
    article = db.relationship(
        'Article', lazy='subquery', backref=db.backref(
            'category', lazy='joined')
    )

    def __repr__(self):
        return '<Category %r>' % self.name

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
