from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, ForeignKey, Text

from app.core.db import Base
from .abstract import SomeTask, SomeTaskUserAssociation

if TYPE_CHECKING:
    from app.models.user import User


class TaskQuestionUserAssociation(SomeTaskUserAssociation):
    """Модель тестов АПИ - пользователей."""

    __tablename__ = 'task_question_user_assoc'

    answer: Mapped['Answer'] = relationship(
        back_populates='task_test_user',
    )
    task: Mapped['TaskTest'] = Column(ForeignKey('task_test_question.id'))
    user: Mapped['User'] = Column(ForeignKey('user.id'))


class Answer(Base):
    """Ответы для теста."""

    __tablename__ = 'task_test_answer'

    test: Mapped['Question'] = Column(ForeignKey('task_test_question.id'))
    value: str = Column(Text, nullable=False)


class Question(Base):
    """Модель вопроса теста."""

    __tablename__ = 'task_test_question'

    test: Mapped['TaskTest'] = Column(ForeignKey('task_test.id'))
    users: Mapped[list['TaskQuestionUserAssocation']] = relationship(
        back_populates='task_question',
    )
    quation: str = Column(Text, nullable=False)
    answers: Mapped[list['Answer']] = relationship(
        back_populates='question',
    )
    correct_answer: Mapped['Answer'] = relationship()


class TaskTest(SomeTask):
    """Модель всего теста."""

    __tablename__ = 'task_test'

    questions: Mapped[list['Question']] = relationship(
        back_populates='test',
    )
