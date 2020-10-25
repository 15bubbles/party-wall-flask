from party_wall.db import db
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(UUID, primary_key=True)
