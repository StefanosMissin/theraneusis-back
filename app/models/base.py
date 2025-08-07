from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String
import uuid

class TenantBase:
    @declared_attr
    def tenant_id(cls):
        return Column(String, nullable=False, index=True)

    @declared_attr
    def id(cls):
        return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
