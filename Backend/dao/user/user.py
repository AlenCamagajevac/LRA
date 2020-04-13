from core.enum.role_enum import RoleTypes
from dao.base.base_model import BaseModel
from dao.user.role import Role
from db import db
from dao.user.user_roles import user_roles
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import DateTime
from sqlalchemy.sql import expression
from datetime import datetime


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # N to N relationship with roles
    roles = db.relationship(
        'Role', secondary=user_roles, lazy='joined', backref=db.backref(
            'users', lazy=True)
    )
    # One to N relationship with articles
    articles = db.relationship(
        'Article', lazy='subquery', backref=db.backref(
            'user', lazy='joined')
    )
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(200), unique=False, nullable=True)

    # Account confirmation
    confirmed = db.Column(
        db.Boolean, nullable=False, server_default=expression.false())
    confirmed_date = db.Column(DateTime, nullable=True)

    # Notifications
    allow_mail_notifications = db.Column(
        db.Boolean, nullable=False, server_default=expression.true())
    allow_push_notifications = db.Column(
        db.Boolean, nullable=False, server_default=expression.true())

    @classmethod
    def find_with_mail_notifications_enabled(cls):
        return cls.query.filter_by(
            allow_mail_notifications=True).filter_by(confirmed=True).all()

    @classmethod
    def find_with_push_notifications_enabled(cls):
        return cls.query.filter_by(
            allow_push_notifications=True).filter_by(confirmed=True).all()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def find_all_users(cls, page, per_page):
        return cls.query.filter(
            User.roles.any(Role.role_type == RoleTypes.CLIENT)
        ).paginate(page, per_page, error_out=False)

    def confirm_account(self):
        self.confirmed = True
        self.confirmed_date = datetime.utcnow()

    def add_to_role(self, role: RoleTypes):
        role = Role.find_by_type(role)
        self.roles.append(role)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.email
