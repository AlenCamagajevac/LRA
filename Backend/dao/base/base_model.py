from db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from uuid import uuid4


class BaseModel(db.Model):
    __abstract__ = True

    uuid = db.Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid4
    )
    created_date = db.Column(DateTime, default=datetime.utcnow())
    last_update = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now()
    )
