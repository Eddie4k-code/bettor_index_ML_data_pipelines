"""Shared team-bet snapshot request/result shapes and base pregame record fields."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from sport_keys import normalize_sport_key

ALLOWED_BOOKMAKERS: frozenset[str] = frozenset({
    "draftkings",
    "fanduel",
    "betmgm",
    "fanatics",
})


class SnapshotRequest(BaseModel):
    """Input to the snapshot pipeline for one sport/market at a fixed observation time."""

    model_config = ConfigDict(frozen=True)

    sport_key: str
    market_key: str
    observation_time: datetime

    @property
    def normalized_sport_key(self) -> str:
        return normalize_sport_key(self.sport_key)


class SnapshotRunResult(BaseModel):
    """Aggregate counts logged after a snapshot pipeline run."""

    model_config = ConfigDict(frozen=True)

    candidates: int
    snapshotted: int
    skipped_existing: int
    skipped_leakage: int


class TeamBetSnapshotRecordBase(BaseModel):
    """Fields shared by every persisted team-bet pregame snapshot row."""

    model_config = ConfigDict(from_attributes=True, frozen=True, extra="forbid")

    observation_time: datetime
    event_id: str
    sport_key: str
    market_key: str
    bookmaker: str
    outcome_name: str
    commence_time: datetime
    outcome_point: float | None
    outcome_price: float
    market_last_update: datetime
    home_team: str
    away_team: str
    home_team_id: int | None = None
    away_team_id: int | None = None
    outcome_team_id: int | None = None
    hit_rate_market_last_update: datetime
    snapshot_version: str
    created_at: datetime
    season: int | None = None
