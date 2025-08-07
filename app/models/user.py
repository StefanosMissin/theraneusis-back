from sqlalchemy import Column, String, Enum, Boolean
from app.core.database import Base
from app.models.base import TenantBase
import enum

class UserRole(str, enum.Enum):
    doctor = "doctor"
    client = "client"
    admin = "admin"

class User(TenantBase, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.client)
    is_verified = Column(Boolean, default=False)
