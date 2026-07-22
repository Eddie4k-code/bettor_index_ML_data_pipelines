"""Read DTOs mirroring upstream featured odds and team-bet hit-rate row shapes."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FeaturedOddsRow(BaseModel):
    """Point-in-time featured odds row passed into snapshot builders."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str
    bookmaker: str
    market_key: str
    outcome_name: str
    sport_key: str
    commence_time: datetime
    outcome_price: float
    outcome_point: float | None
    market_last_update: datetime
    home_team: str
    away_team: str
    home_team_id: int | None = None
    away_team_id: int | None = None


class TeamBetHitRateRowBase(BaseModel):
    """Identity fields shared by every upstream team-bet hit-rate row."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str
    bookmaker: str
    market_key: str
    outcome_name: str
    market_last_update: datetime


class TeamBetH2hHitRateRow(TeamBetHitRateRowBase):
    home_team: str
    away_team: str
    home_team_id: int | None = None
    away_team_id: int | None = None
    outcome_team_id: int | None = None
    last_n_wins: int | None = None
    last_n_losses: int | None = None
    last_n_sample: int | None = None
    last_n_window: int | None = None
    venue_wins: int | None = None
    venue_losses: int | None = None
    venue_sample: int | None = None
    venue_window: int | None = None
    venue_type: str | None = None
    h2h_wins: int | None = None
    h2h_losses: int | None = None
    h2h_sample: int | None = None
    h2h_window: int | None = None


class TeamBetSpreadsHitRateRow(TeamBetHitRateRowBase):
    home_team: str
    away_team: str
    home_team_id: int | None = None
    away_team_id: int | None = None
    outcome_team_id: int | None = None
    spread: float
    last_n_covers: int
    last_n_sample: int
    last_n_window: int
    h2h_covers: int
    h2h_sample: int
    h2h_window: int
    venue_covers: int
    venue_sample: int
    venue_window: int
    venue_type: str


class TeamBetTotalsHitRateRow(TeamBetHitRateRowBase):
    home_team: str
    away_team: str
    home_team_id: int | None = None
    away_team_id: int | None = None
    direction: str
    line: float
    configured_window: int
    home_team_clears: int
    home_team_sample: int
    away_team_clears: int
    away_team_sample: int
    h2h_window: int
    h2h_sample: int
    h2h_clears: int
    h2h_avg_total: float | None = None
