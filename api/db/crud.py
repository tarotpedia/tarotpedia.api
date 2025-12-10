from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.db.models import CardInterpretation, NumerologyData, Reading, ReadingCard, ReadingSummary
from api.models.tarot import TarotCard, TarotInterpretation


async def create_reading(
    db: AsyncSession,
    user_name: str,
    user_dob: date,
    question: str,
    cards: List[TarotCard],
    interpretations: List[TarotInterpretation],
    summary: str,
    numerology_meaning: Optional[str] = None,
) -> UUID:
    reading = Reading(user_name=user_name, user_dob=user_dob, question=question)

    db.add(reading)
    await db.flush()

    position_map = {0: "past", 1: "present", 2: "future"}

    for idx, card in enumerate(cards):
        position = position_map.get(idx, f"card_{idx}")
        reading_card = ReadingCard(
            reading_id=reading.id,
            position=position,
            card_name=card.name,
            is_upright=card.is_upright,
            image_url=card.image_url,
            full_card_name=card.full_card_name,
        )
        db.add(reading_card)

    for interp in interpretations:
        card_interpretation = CardInterpretation(
            reading_id=reading.id,
            card_name=interp.card_name,
            position=interp.position,
            orientation=interp.orientation,
            meaning=interp.meaning,
        )
        db.add(card_interpretation)

    reading_summary = ReadingSummary(reading_id=reading.id, summary=summary)
    db.add(reading_summary)

    if numerology_meaning:
        numerology_data = NumerologyData(reading_id=reading.id, numerology_meaning=numerology_meaning)
        db.add(numerology_data)

    await db.commit()
    return reading.id


async def get_reading(db: AsyncSession, reading_id: UUID) -> Optional[Reading]:
    stmt = (
        select(Reading)
        .options(
            selectinload(Reading.cards),
            selectinload(Reading.interpretations),
            selectinload(Reading.summary),
            selectinload(Reading.numerology),
        )
        .where(Reading.id == reading_id)
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()
