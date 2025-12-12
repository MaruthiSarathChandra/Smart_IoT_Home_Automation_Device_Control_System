from sqlalchemy import Column, Integer, String, Boolean
from ..repo.connection import Base


class User(Base):
    __tablename__ = "usersdb"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gmail_id = Column(String(100), nullable=False)
    password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User id={self.id} gmail={self.gmail_id}>"


