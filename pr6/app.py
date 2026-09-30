from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Table(BaseModel):
    id: int
    number: int = Field(description="Номер столика в зале")
    capacity: int = Field(description="Максимальное количество гостей")
    is_available: bool = Field(description="Доступен ли столик прямо сейчас")


class ReservationRequest(BaseModel):
    guest_name: str = Field()
    guest_phone: str = Field()
    table_id: int = Field()
    guests_count: int = Field()
    reservation_time: datetime = Field()


class Reservation(ReservationRequest):
    id: int = Field(description="Уникальный ID бронирования")
    status: str = Field(description="Статус бронирования")


class ErrorResponse(BaseModel):
    error: str = Field()
    message: str = Field()


app = FastAPI(
    title="API Бронирования столиков в ресторане",
    description="Спецификация для управления бронированием столов. Позволяет просматривать столики и создавать бронирования.",
    version="1.0.0",
)


tables_db: List[Table] = [
    Table(id=1, number=5, capacity=4, is_available=True),
    Table(id=2, number=12, capacity=2, is_available=False),
]
reservations_db: dict[int, Reservation] = {}
next_reservation_id = 101


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": f"HTTP {exc.status_code}", "message": exc.detail},
    )


@app.get(
    "/tables",
    response_model=List[Table],
    summary="Получить список всех столиков",
    description="Возвращает информацию о всех столиках ресторана и их вместимости.",
)
def get_tables():
    return tables_db


@app.post(
    "/reservations",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое бронирование",
    description="Отправляет запрос на бронирование конкретного столика.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Ошибка валидации (например, столик уже занят)",
        }
    },
)
def create_reservation(reservation: ReservationRequest):
    global next_reservation_id

    table = next((t for t in tables_db if t.id == reservation.table_id), None)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Столик с ID {reservation.table_id} не найден.",
        )

    if not table.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Столик с ID {reservation.table_id} уже забронирован на это время.",
        )

    new_reservation = Reservation(
        id=next_reservation_id, **reservation.model_dump(), status="confirmed"
    )

    reservations_db[next_reservation_id] = new_reservation
    next_reservation_id += 1

    return new_reservation


@app.get(
    "/reservations/{reservation_id}",
    response_model=Reservation,
    summary="Получить информацию о бронировании по ID",
    responses={404: {"model": ErrorResponse, "description": "Бронирование не найдено"}},
)
def get_reservation(reservation_id: int):
    reservation = reservations_db.get(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронирование с ID {reservation_id} не найдено.",
        )
    return reservation
