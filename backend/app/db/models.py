from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class DiaryEntry(Base):
    __tablename__ = "diary_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime)

    user = relationship("User")

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
