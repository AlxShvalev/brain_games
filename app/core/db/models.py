import uuid

from sqlalchemy import BOOLEAN, DATE, TIMESTAMP, Column, Integer, String, func
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

    username = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100))
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(70), nullable=False)
    is_superuser = Column(BOOLEAN, default=False, nullable=False)
    is_staff = Column(BOOLEAN, default=False, nullable=False)
    date_of_birth = Column(DATE)
    last_login_at = Column(TIMESTAMP)
    teams = relationship("Team", back_populates="owner")
    games = relationship("Game", back_populates="editor")
    questions = relationship("Question", back_populates="author")

    def __repr__(self):
        return f"User (username: {self.username}, email: {self.email})"


class Team(Base):
    """Модель для описания Команды."""

    title = Column(String(500), nullable=False, unique=True)
    city = Column(String(100))
    owner_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="teams")
    games = relationship("TeamsGames", back_populates="teams")
    answers = relationship("Answer", back_populates="team")

    def __repr__(self):
        return self.title


class Game(Base):
    """Модель для описания Игры."""

    title = Column(String, nullable=False, unique=True)
    date_of = Column(DATE, nullable=False)
    editor_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    editor = relationship("User", back_populates="games")
    questions = relationship("GameQuestions", back_populates="game", order_by="GameQuestions.question_number")
    teams = relationship("TeamsGames", back_populates="games")
    answers = relationship("Answer", back_populates="game")

    def __repr__(self):
        return self.title


class TeamsGames(Base):
    """Связь между командами и играми."""

    team_id = Column(UUID(as_uuid=True), ForeignKey(Team.id, ondelete="CASCADE"), nullable=False)
    teams = relationship("Team", back_populates="games")
    game_id = Column(UUID(as_uuid=True), ForeignKey(Game.id, ondelete="CASCADE"), nullable=False)
    games = relationship("Game", back_populates="teams")
    team_number = Column(Integer, nullable=False)


class Question(Base):
    """Модель для описания Вопроса."""

    author_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="questions")
    text = Column(String(2048), nullable=False)
    answer = Column(String(500), nullable=False)
    comment = Column(String(2048))
    games = relationship("GameQuestions", back_populates="question")
    answers = relationship("Answer", back_populates="question")


class GameQuestions(Base):
    """Модель для описания вопросов для игры."""

    question_number = Column(Integer, nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey(Game.id, ondelete="CASCADE"), nullable=False)
    game = relationship("Game", back_populates="questions")
    question_id = Column(UUID(as_uuid=True), ForeignKey(Question.id, ondelete="CASCADE"), nullable=False)
    question = relationship("Question", back_populates="games")


class Answer(Base):
    """Модель для описания Ответа."""

    text = Column(String(500))
    is_correct = Column(BOOLEAN, nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey(Game.id, ondelete="CASCADE"), nullable=False)
    game = relationship("Game", back_populates="answers")
    team_id = Column(UUID(as_uuid=True), ForeignKey(Team.id, ondelete="CASCADE"), nullable=False)
    team = relationship("Team", back_populates="answers")
    question_id = Column(UUID(as_uuid=True), ForeignKey(Question.id, ondelete="CASCADE"), nullable=False)
    question = relationship("Question", back_populates="answers")
