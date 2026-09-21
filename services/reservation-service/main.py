from datetime import datetime
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Reservation Service",
    description="Microservicio para la gestión de reservas",
    version="1.0.0"
)


class ReservationCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    resource: str = Field(min_length=2, max_length=100)
    reservation_date: datetime


class Reservation(ReservationCreate):
    id: UUID


reservations: dict[UUID, Reservation] = {}


@app.get("/")
def root():
    return {
        "service": "reservation-service",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/reservations", response_model=Reservation, status_code=201)
def create_reservation(data: ReservationCreate):
    reservation = Reservation(
        id=uuid4(),
        **data.model_dump()
    )

    reservations[reservation.id] = reservation

    return reservation



@app.get("/reservations", response_model=list[Reservation])
def list_reservations():
    return list(reservations.values())


@app.get("/reservations/{reservation_id}", response_model=Reservation)
def get_reservation(reservation_id: UUID):
    reservation = reservations.get(reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    return reservation

@app.delete("/reservations/{reservation_id}", status_code=204)
def cancel_reservation(reservation_id: UUID):
    reservation = reservations.get(reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    del reservations[reservation_id]