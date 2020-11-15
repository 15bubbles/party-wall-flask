import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from party_wall.db import db


# perhaps superuser field should not be here bot in some Superusers table which will be one to one with Users table
# perhaps email should also be unique
class UserModel(db.Model):
    __tablename__ = "auth_users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4
    )
    username = Column(String(length=255), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    authenticated = Column(Boolean, nullable=False, default=False)
    superuser = Column(Boolean, nullable=False, default=False)
