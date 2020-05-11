from dao.base.base_model import BaseModel
from sqlalchemy.sql import expression
from sqlalchemy.dialects.postgresql import UUID
from db import db


class Image(BaseModel):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    is_cover = db.Column(
        db.Boolean, nullable=False, server_default=expression.false())
    storage_id = db.Column(
        UUID(as_uuid=True), unique=True, nullable=False
    )
    article_id = db.Column(
        db.Integer, db.ForeignKey('articles.id'), nullable=False)
