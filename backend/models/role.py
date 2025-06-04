# backend/models/role.py
from sqlalchemy import Column, Integer, String
from backend.models.order import Base # Usamos la misma Base

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.role_name}>'