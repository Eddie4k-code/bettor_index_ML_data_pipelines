"""Parameterized read repository for graded team-bet export pairs."""

from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from interfaces.team_bet_graded_export_read_repository_interface import (
    TeamBetGradedExportReadRepositoryInterface,
)
from repositories.team_bets._graded_export_reads import fetch_graded_export_pairs
from schemas.export import GradedExportPair

TSnapshot = TypeVar("TSnapshot", bound=BaseModel)
TGrade = TypeVar("TGrade", bound=BaseModel)


class TeamBetGradedExportReadRepository(
    TeamBetGradedExportReadRepositoryInterface[TSnapshot, TGrade],
):
    def __init__(
        self,
        db: Session,
        *,
        snapshot_model: type,
        grade_model: type,
        snapshot_record_cls: type[TSnapshot],
        grade_record_cls: type[TGrade],
    ):
        self.db = db
        self.snapshot_model = snapshot_model
        self.grade_model = grade_model
        self.snapshot_record_cls = snapshot_record_cls
        self.grade_record_cls = grade_record_cls

    def fetch_graded_pairs(
        self,
        *,
        observation_time_start: datetime | None = None,
        observation_time_end: datetime | None = None,
        commence_time_start: datetime | None = None,
        commence_time_end: datetime | None = None,
    ) -> list[GradedExportPair[TSnapshot, TGrade]]:
        return fetch_graded_export_pairs(
            self.db,
            snapshot_model=self.snapshot_model,
            grade_model=self.grade_model,
            snapshot_record_cls=self.snapshot_record_cls,
            grade_record_cls=self.grade_record_cls,
            observation_time_start=observation_time_start,
            observation_time_end=observation_time_end,
            commence_time_start=commence_time_start,
            commence_time_end=commence_time_end,
        )
