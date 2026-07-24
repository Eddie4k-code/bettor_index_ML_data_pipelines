"""Shared team-bet export request/result shapes and partition manifest metadata."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

TSnapshot = TypeVar("TSnapshot", bound=BaseModel)
TGrade = TypeVar("TGrade", bound=BaseModel)

# Columns written from grade rows; training code must drop these from feature matrices.
EXPORT_LABEL_COLUMNS: tuple[str, ...] = (
    "grade_outcome",
    "grade_version",
    "home_team_score",
    "away_team_score",
    "graded_at",
)


class GradedExportPair(BaseModel, Generic[TSnapshot, TGrade]):
    """Snapshot feature row joined to its matching post-game grade label row."""

    model_config = ConfigDict(frozen=True)

    snapshot: TSnapshot
    grade: TGrade


class ExportRequest(BaseModel):
    """Input to the export pipeline for one sport/market with optional temporal filters."""

    model_config = ConfigDict(frozen=True)

    sport_key: str
    market_key: str
    output_dir: str
    observation_time_start: datetime | None = None
    observation_time_end: datetime | None = None
    commence_time_start: datetime | None = None
    commence_time_end: datetime | None = None


class ExportRunResult(BaseModel):
    """Aggregate counts logged after an export pipeline run."""

    model_config = ConfigDict(frozen=True)

    candidates: int
    exported: int
    partitions_written: int
    skipped_empty: int


class ExportManifest(BaseModel):
    """Metadata written beside each exported partition for reproducibility."""

    model_config = ConfigDict(frozen=True)

    row_count: int
    sport_key: str
    market_key: str
    observation_time_start: datetime | None
    observation_time_end: datetime | None
    commence_time_start: datetime | None
    commence_time_end: datetime | None
    snapshot_versions: list[str]
    grade_versions: list[str]
    feature_columns: list[str]
    label_columns: list[str]
    git_sha: str | None = None
    exported_at: datetime
