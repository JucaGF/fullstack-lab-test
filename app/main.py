"""API de eventos com persistência SQLite."""

from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Base, make_engine
from app.models import Event, Registration
from app.registrations import router as registrations_router


class EventInput(BaseModel):
    title: str = Field(min_length=1)
    date: date
    capacity: int = Field(gt=0)


def create_app(database_url: str = "sqlite://") -> FastAPI:
    """Cria a API; testes usam banco isolado, o servidor usa um arquivo."""
    app = FastAPI(title="Eventos do Trilha")
    engine = make_engine(database_url)
    Base.metadata.create_all(engine)
    app.state.engine = engine
    app.include_router(registrations_router)

    def event_response(event: Event, session: Session):
        registered = session.scalar(
            select(func.count(Registration.id)).where(Registration.event_id == event.id)
        )
        return {
            "id": event.id,
            "title": event.title,
            "date": event.date.isoformat(),
            "capacity": event.capacity,
            "available_slots": event.capacity - registered,
        }

    @app.get("/events")
    def list_events():
        with Session(engine) as session:
            return [event_response(event, session) for event in session.scalars(select(Event).order_by(Event.id))]

    @app.get("/events/{event_id}")
    def get_event(event_id: int):
        with Session(engine) as session:
            event = session.get(Event, event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Evento não encontrado")
            return event_response(event, session)

    @app.post("/events", status_code=201)
    def create_event(data: EventInput):
        with Session(engine) as session:
            event = Event(**data.model_dump())
            session.add(event)
            session.commit()
            session.refresh(event)
            return event_response(event, session)

    return app


app = create_app("sqlite:///events.db")
