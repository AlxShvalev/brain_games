import uuid
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.schema import ForeignKey


@as_declarative()
class Base:
    """Base model."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp()
    )
    __name__: str


class Command(Base):
    """Модель для описания Команды."""
    title = Column()
    city = Column()
    players = relationship("Player", back_populates="commands")
    answers = relationship("Answer", back_populates="command")


class Player(Base):
    """Модель для описания Игрока."""
    pass


class Game(Base):
    """Модель для описания Игры."""
    title = Column(String, )
    questions = relationship("Question", back_populates="game")
    answers = relationship("Answer", back_populates="game")


class Question(Base):
    """Модель для описания Вопроса."""
    number = Column(Integer)
    text = Column(String(2048), nullable=False)
    answer = Column(String(500), nullable=False)
    comment = Column(String(2048), nullable=True)
    game = relationship("Game", back_populates="questions")


class Answer(Base):
    """Модель для описания Ответа."""
    text = Column(String)
    command = relationship("Command", back_populates="answers")
