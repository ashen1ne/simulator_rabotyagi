from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from typing import Optional
from app.enums import Status


class RabotyagaBase(BaseModel):
    rabotyaga_name: str = Field(..., min_length=1, max_length=50)
    hourly_rate: float = Field(600, ge=1, le=1_000_000)
    total_balance: float = Field(0, ge=0)


class RabotyagaCreate(RabotyagaBase):
    pass


class RabotyagaResponse(RabotyagaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RabotyagaUpdate(BaseModel):
    rabotyaga_name: str | None = Field(None, min_length=1, max_length=50)
    hourly_rate: float | None = Field(None, ge=1, le=1_000_000)
    total_balance: float | None = Field(None, ge=0)


class SmenaBase(BaseModel):
    start_smena: datetime
    status: Status = Status.zaplanorivona


class SmenaCreate(SmenaBase):
    rabotyaga_id: int


class SmenaResponse(SmenaBase):
    id: int
    rabotyaga_id: int
    actual_start: datetime | None = None
    actual_end: datetime | None = None
    zarabotok: float = 0

    model_config = ConfigDict(from_attributes=True)
    

class ScheduleCreate(BaseModel):
    rabotyaga_id: int
    start_date: datetime = Field(default_factory=datetime.now) 
    count_months: int = Field(2, ge=1, le=12)

    @field_validator("start_date")
    @classmethod
    def validate_date(cls, v: datetime):
        if v.date() < datetime.now().date():
            raise ValueError("Нельзя составить график на прошедшее время")
        return v
