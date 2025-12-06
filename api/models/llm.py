from pydantic import BaseModel, Field


class NumerologyLLMResponse(BaseModel):
    """Structured response for numerology readings to ensure consistent format."""

    calculations: str = Field(
        description="Formatted calculation breakdown showing Expression Number, Life Path Number, Personal Year Number, and Personal Numerology"
    )
    insight: str = Field(
        description="Brief 2-3 sentence insight about what the numbers reveal, mentioning the cosmic signature for tarot"
    )


class TarotLLMResponse(BaseModel):
    past: str
    present: str
    future: str
    summary: str
