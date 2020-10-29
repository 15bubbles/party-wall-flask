from uuid import uuid4

from party_wall.db import db
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
