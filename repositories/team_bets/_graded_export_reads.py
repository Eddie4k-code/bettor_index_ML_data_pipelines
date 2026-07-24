"""Shared INNER JOIN query for exportable snapshot rows with matching grades."""

from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Query, Session

from schemas.export import GradedExportPair

TSnapshot = TypeVar("TSnapshot", bound=BaseModel)
TGrade = TypeVar("TGrade", bound=BaseModel)


def _snapshot_grade_join_condition(snapshot_model: type, grade_model: type):
    return (
        (snapshot_model.observation_time == grade_model.observation_time)
        & (snapshot_model.event_id == grade_model.event_id)
        & (snapshot_model.bookmaker == grade_model.bookmaker)
        & (snapshot_model.outcome_name == grade_model.outcome_name)
        & (snapshot_model.snapshot_version == grade_model.snapshot_version)
    )


def apply_export_temporal_filters(
    query: Query,
    *,
    snapshot_model: type,
    observation_time_start: datetime | None = None,
    observation_time_end: datetime | None = None,
    commence_time_start: datetime | None = None,
    commence_time_end: datetime | None = None,
) -> Query:
    if observation_time_start is not None:
        query = query.filter(snapshot_model.observation_time >= observation_time_start)
    if observation_time_end is not None:
        query = query.filter(snapshot_model.observation_time <= observation_time_end)
    if commence_time_start is not None:
        query = query.filter(snapshot_model.commence_time >= commence_time_start)
    if commence_time_end is not None:
        query = query.filter(snapshot_model.commence_time <= commence_time_end)
    return query


def fetch_graded_export_pairs(
    db: Session,
    *,
    snapshot_model: type,
    grade_model: type,
    snapshot_record_cls: type[TSnapshot],
    grade_record_cls: type[TGrade],
    observation_time_start: datetime | None = None,
    observation_time_end: datetime | None = None,
    commence_time_start: datetime | None = None,
    commence_time_end: datetime | None = None,
) -> list[GradedExportPair[TSnapshot, TGrade]]:
    query = db.query(snapshot_model, grade_model).join(
        grade_model,
        _snapshot_grade_join_condition(snapshot_model, grade_model),
    )
    query = apply_export_temporal_filters(
        query,
        snapshot_model=snapshot_model,
        observation_time_start=observation_time_start,
        observation_time_end=observation_time_end,
        commence_time_start=commence_time_start,
        commence_time_end=commence_time_end,
    )
    return [
        GradedExportPair(
            snapshot=snapshot_record_cls.model_validate(snapshot_row),
            grade=grade_record_cls.model_validate(grade_row),
        )
        for snapshot_row, grade_row in query.all()
    ]
