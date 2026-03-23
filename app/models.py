from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime, Enum
from app.core.db import Base
from datetime import datetime
from app.enums import Status


class Rabotyaga(Base):
    __tablename__ = "rabotyagi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rabotyaga_name: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255))
    hourly_rate: Mapped[float] = mapped_column(nullable=False, default=600)
    total_balance: Mapped[float] = mapped_column(nullable=False, default=0)

    smeny: Mapped[list["Smena"]] = relationship(back_populates="rabotyaga")


class Smena(Base):
    __tablename__ = "smeny"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    rabotyaga_id: Mapped[int] = mapped_column(
        ForeignKey("rabotyagi.id"), nullable=False
    )
    start_smena: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[Status] = mapped_column(
        Enum(Status), nullable=False, default=Status.zaplanorivona
    )
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    zarabotok: Mapped[float] = mapped_column(nullable=False, default=0)

    rabotyaga: Mapped["Rabotyaga"] = relationship(back_populates="smeny")
