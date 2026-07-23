"""ABC contracts for sport-agnostic team-bet grade builders."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar

from schemas.games import CompletedGameRow
from schemas.grade import TeamBetGradeRecordBase
from schemas.snapshot import TeamBetSnapshotRecordBase

TGradeRecord = TypeVar("TGradeRecord", bound=TeamBetGradeRecordBase)


class H2hGradeBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        *,
        snapshot: TeamBetSnapshotRecordBase,
        game: CompletedGameRow,
        record_cls: type[TGradeRecord],
        graded_at: datetime,
        created_at: datetime,
    ) -> TGradeRecord | None:
        """Return a grade row or None when the snapshot outcome cannot be resolved."""


class SpreadsGradeBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        *,
        snapshot: TeamBetSnapshotRecordBase,
        game: CompletedGameRow,
        record_cls: type[TGradeRecord],
        graded_at: datetime,
        created_at: datetime,
    ) -> TGradeRecord | None:
        """Return a grade row or None when spread/outcome resolution fails."""


class TotalsGradeBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        *,
        snapshot: TeamBetSnapshotRecordBase,
        game: CompletedGameRow,
        record_cls: type[TGradeRecord],
        graded_at: datetime,
        created_at: datetime,
    ) -> TGradeRecord | None:
        """Return a grade row or None when direction/line resolution fails."""
