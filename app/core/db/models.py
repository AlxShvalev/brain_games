import enum
import uuid

from sqlalchemy import DATE, TIMESTAMP, Column, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.schema import ForeignKey


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
    """Модель пользователя."""

    class Role(str, enum.Enum):
        ADMIN = "admin"
        STUFF = "stuff"
        USER = "user"

    username = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100))
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(70), nullable=False)
    role = Column(Enum(Role, name="user_role", values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    date_of_birth = Column(DATE)
    last_login_at = Column(TIMESTAMP)

    def __repr__(self):
        return self.username


class Command(Base):
    """Модель для описания Команды."""

    title = Column(String(500), nullable=False, unique=True)
    city = Column(String(100))
    players = relationship("Player", back_populates="commands")
    answers = relationship("Answer", back_populates="command")

    def __repr__(self):
        return self.title


class Player(Base):
    """Модель для описания Игрока."""

    pass


class Game(Base):
    """Модель для описания Игры."""

    title = Column(String, nullable=False, unique=True)
    date_of = Column(DATE, nullable=False)
    questions = relationship("Question", back_populates="game")
    answers = relationship("Answer", back_populates="game")

    def __repr__(self):
        return self.title


class Question(Base):
    """Модель для описания Вопроса."""

    author_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="questions")
    text = Column(String(2048), nullable=False)
    answer = Column(String(500), nullable=False)
    comment = Column(String(2048))
    game = relationship("Game", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    """Модель для описания Ответа."""

    text = Column(String(500))
    command_id = Column(UUID(as_uuid=True), ForeignKey(Command.id, ondelete="CASCADE"), nullable=False)
    command = relationship("Command", back_populates="answers")
    question_id = Column(UUID(as_uuid=True), ForeignKey(Question.id, ondelete="CASCADE"), nullable=False)
    question = relationship("Question", back_populates="answers")
