"""ABC contracts for sport-agnostic team-bet snapshot builders."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.upstream_rows import (
    FeaturedOddsRow,
    TeamBetH2hHitRateRow,
    TeamBetSpreadsHitRateRow,
    TeamBetTotalsHitRateRow,
)

TH2hRecord = TypeVar("TH2hRecord", bound=TeamBetSnapshotRecordBase)
TSpreadsRecord = TypeVar("TSpreadsRecord", bound=TeamBetSnapshotRecordBase)
TTotalsRecord = TypeVar("TTotalsRecord", bound=TeamBetSnapshotRecordBase)


class H2hSnapshotBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        *,
        observation_time: datetime,
        odds: FeaturedOddsRow,
        hit_rate: TeamBetH2hHitRateRow,
        record_cls: type[TH2hRecord],
        created_at: datetime,
    ) -> TH2hRecord | None:
        """Return a snapshot row or None when temporal/join rules reject the pair."""


class SpreadsSnapshotBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        *,
        observation_time: datetime,
        odds: FeaturedOddsRow,
        hit_rate: TeamBetSpreadsHitRateRow,
        record_cls: type[TSpreadsRecord],
        created_at: datetime,
    ) -> TSpreadsRecord | None:
        """Return a snapshot row or None when temporal/join/line rules reject the pair."""


class TotalsSnapshotBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        *,
        observation_time: datetime,
        odds: FeaturedOddsRow,
        hit_rate: TeamBetTotalsHitRateRow,
        record_cls: type[TTotalsRecord],
        created_at: datetime,
    ) -> TTotalsRecord | None:
        """Return a snapshot row or None when temporal/join/line rules reject the pair."""
