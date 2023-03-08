from sqlalchemy import Column, String, Integer, SmallInteger, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from server.src.database import Base

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), primary_key=True, unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    category = relationship("TaskCategory", cascade="all,delete", backref="user")