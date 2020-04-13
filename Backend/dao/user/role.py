
from dao.base.base_model import BaseModel
from db import db
from core.enum.role_enum import RoleTypes


class Role(BaseModel):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.Enum(RoleTypes))
    description = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name

    @classmethod
    def find_by_type(cls, role_type: RoleTypes):
        return cls.query.filter_by(role_type=role_type).first()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
