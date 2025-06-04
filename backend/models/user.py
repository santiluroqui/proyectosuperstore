# backend/models/user.py
from sqlalchemy import Column, Integer, String
from backend.models.order import Base # Usamos la misma Base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, ForeignKey

# Tabla intermedia para la relación muchos a muchos entre User y Role
# (Aunque en este proyecto no la usarás directamente, es buena práctica)
user_roles = Table(
    'user_roles',
    Base.metadata, # Asegúrate de que use la misma metadata de Base
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.role_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False) # ¡En una app real, siempre hashea las contraseñas!

    # Relación a los roles
    roles = relationship('Role', secondary=user_roles, backref='users')

    def __repr__(self):
        return f'<User {self.username}>'