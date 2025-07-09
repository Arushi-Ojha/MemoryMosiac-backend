from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Time, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    journals = relationship("Journal", back_populates="owner")


class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="journals")

    entries = relationship("Entry", back_populates="journal", cascade="all, delete")


class Entry(Base):
    __tablename__ = "entries"

    page_number = Column(Integer, nullable=False)
    book_id = Column(Integer, ForeignKey("journals.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    mood = Column(String(50))
    story = Column(Text)

    journal = relationship("Journal", back_populates="entries")
    __table_args__ = (
        PrimaryKeyConstraint('book_id', 'page_number'),
    )
