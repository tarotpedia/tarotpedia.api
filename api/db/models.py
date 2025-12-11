import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.db.database import Base


class Reading(Base):
    __tablename__ = "readings"

    reading_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String(255), nullable=False)
    user_birth_date = Column(Date, nullable=False)
    question_text = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(
        Text,
        nullable=False,
        default=lambda: datetime.utcnow().isoformat(),
        onupdate=lambda: datetime.utcnow().isoformat(),
    )

    cards = relationship("ReadingCard", back_populates="reading", cascade="all, delete-orphan")
    interpretations = relationship("CardInterpretation", back_populates="reading", cascade="all, delete-orphan")
    summary = relationship("ReadingSummary", back_populates="reading", uselist=False, cascade="all, delete-orphan")
    numerology = relationship("NumerologyData", back_populates="reading", uselist=False, cascade="all, delete-orphan")


class ReadingCard(Base):
    __tablename__ = "reading_cards"
    __table_args__ = (UniqueConstraint("reading_id", "card_position_text", name="uq_reading_position"),)

    reading_card_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reading_id = Column(UUID(as_uuid=True), ForeignKey("readings.reading_id", ondelete="CASCADE"), nullable=False)
    card_position_text = Column(String(20), nullable=False)
    card_name = Column(String(255), nullable=False)
    is_upright = Column(Boolean, nullable=False)
    card_image_url = Column(String(500))
    full_card_name = Column(String(300), nullable=False)
    created_at = Column(Text, nullable=False, default=lambda: datetime.utcnow().isoformat())

    reading = relationship("Reading", back_populates="cards")


class CardInterpretation(Base):
    __tablename__ = "card_interpretations"
    __table_args__ = (UniqueConstraint("reading_id", "card_position_text", name="uq_interpretation_position"),)

    interpretation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reading_id = Column(UUID(as_uuid=True), ForeignKey("readings.reading_id", ondelete="CASCADE"), nullable=False)
    card_name = Column(String(255), nullable=False)
    card_position_text = Column(String(20), nullable=False)
    card_orientation_text = Column(String(20), nullable=False)
    meaning_text = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False, default=lambda: datetime.utcnow().isoformat())

    reading = relationship("Reading", back_populates="interpretations")


class ReadingSummary(Base):
    __tablename__ = "reading_summaries"

    summary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reading_id = Column(
        UUID(as_uuid=True), ForeignKey("readings.reading_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    summary_text = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False, default=lambda: datetime.utcnow().isoformat())

    reading = relationship("Reading", back_populates="summary")


class NumerologyData(Base):
    __tablename__ = "numerology_entries"

    numerology_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reading_id = Column(
        UUID(as_uuid=True), ForeignKey("readings.reading_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    meaning_text = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False, default=lambda: datetime.utcnow().isoformat())

    reading = relationship("Reading", back_populates="numerology")
