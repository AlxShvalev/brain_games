import uuid

from sqlalchemy import DATE, TIMESTAMP, Column, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship


@as_declarative()
class Base:
    """Base model."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False, onupdate=func.current_timestamp()
    )
    __name__: str


class User(Base):
    """Модель полоьзователя."""

    username = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100))
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(70), nullable=False)
    date_of_birth = Column(DATE)
    last_login_at = Column(TIMESTAMP)

    def __repr__(self) -> str:
        return f"{self.name} {self.surname}"


class Command(Base):
    """Модель для описания Команды."""

    title = Column(String(500), nullable=False)
    city = Column(String(100))
    players = relationship("Player", back_populates="commands")
    answers = relationship("Answer", back_populates="command")


class Player(Base):
    """Модель для описания Игрока."""

    pass


class Game(Base):
    """Модель для описания Игры."""

    title = Column(
        String,
    )
    date_of = Column(TIMESTAMP)
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
