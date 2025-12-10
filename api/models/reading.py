from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from api.models.tarot import TarotCard, TarotInterpretation


class SaveReadingRequest(BaseModel):
    user_name: str
    user_dob: date
    question: str
    cards: List[TarotCard]
    interpretations: List[TarotInterpretation]
    summary: str
    numerology_meaning: Optional[str] = None


class SaveReadingResponse(BaseModel):
    reading_id: UUID
    message: str


class ReadingCardResponse(BaseModel):
    position: str
    card_name: str
    is_upright: bool
    image_url: Optional[str]
    full_card_name: str


class CardInterpretationResponse(BaseModel):
    card_name: str
    position: str
    orientation: str
    meaning: str


class GetReadingResponse(BaseModel):
    reading_id: UUID
    user_name: str
    user_dob: date
    question: str
    cards: List[ReadingCardResponse]
    interpretations: List[CardInterpretationResponse]
    summary: str
    numerology_meaning: Optional[str] = None
    created_at: str
