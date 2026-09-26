"""Cria dados pequenos e reproduzíveis para explorar o banco local."""

from datetime import date

from sqlalchemy.orm import Session

from app.database import Base, make_engine
from app.models import Event, User


def seed(engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if session.get(Event, 1) is None:
            session.add(Event(id=1, title="Oficina de Python", date=date(2026, 10, 10), capacity=2))
            session.add(User(id=1, name="Ana", email="ana@example.org"))
            session.add(User(id=2, name="Bruno", email="bruno@example.org"))
            session.commit()


if __name__ == "__main__":
    seed(make_engine())
