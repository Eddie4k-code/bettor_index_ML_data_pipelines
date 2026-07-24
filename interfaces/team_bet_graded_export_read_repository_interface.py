"""ABC for read-only graded snapshot+grade pairs used by export."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

from schemas.export import GradedExportPair

TSnapshot = TypeVar("TSnapshot", bound=BaseModel)
TGrade = TypeVar("TGrade", bound=BaseModel)


class TeamBetGradedExportReadRepositoryInterface(ABC, Generic[TSnapshot, TGrade]):
    @abstractmethod
    def fetch_graded_pairs(
        self,
        *,
        observation_time_start: datetime | None = None,
        observation_time_end: datetime | None = None,
        commence_time_start: datetime | None = None,
        commence_time_end: datetime | None = None,
    ) -> list[GradedExportPair[TSnapshot, TGrade]]:
        """Return inner-joined snapshot and grade rows with optional temporal filters."""
