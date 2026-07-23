"""Shared game read DTOs and completed-status constants for post-game grading."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

COMPLETED_GAME_STATUSES = frozenset({"finished", "status_final", "final"})


class CompletedGameRow(BaseModel):
    """Final scores for one completed game used by grade builders."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    sport_key: str
    status: str
    home_team: str
    away_team: str
    home_team_id: int
    away_team_id: int
    home_team_score: int
    away_team_score: int
    date: datetime
