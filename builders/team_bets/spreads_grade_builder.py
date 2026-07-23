"""Sport-agnostic spread grade builder."""

from datetime import datetime
from typing import TypeVar

from builders.team_bets._grading import (
    grade_spread_outcome,
    resolve_outcome_team_id,
    spread_margin,
    team_and_opponent_scores,
)
from interfaces.team_bet_grade_builder_interfaces import SpreadsGradeBuilderInterface
from schemas.games import CompletedGameRow
from schemas.grade import TeamBetGradeRecordBase
from schemas.snapshot import TeamBetSnapshotRecordBase

TGradeRecord = TypeVar("TGradeRecord", bound=TeamBetGradeRecordBase)


class SpreadsGradeBuilder(SpreadsGradeBuilderInterface):
    def build(
        self,
        *,
        snapshot: TeamBetSnapshotRecordBase,
        game: CompletedGameRow,
        record_cls: type[TGradeRecord],
        graded_at: datetime,
        created_at: datetime,
    ) -> TGradeRecord | None:
        if snapshot.outcome_point is None:
            return None

        outcome_team_id = resolve_outcome_team_id(snapshot)
        if outcome_team_id is None:
            return None

        scores = team_and_opponent_scores(game, outcome_team_id)
        if scores is None:
            return None

        team_score, opponent_score = scores
        margin = spread_margin(team_score, opponent_score, snapshot.outcome_point)
        grade_outcome = grade_spread_outcome(margin)

        return record_cls(
            observation_time=snapshot.observation_time,
            event_id=snapshot.event_id,
            bookmaker=snapshot.bookmaker,
            outcome_name=snapshot.outcome_name,
            snapshot_version=snapshot.snapshot_version,
            grade_outcome=grade_outcome,
            home_team_score=game.home_team_score,
            away_team_score=game.away_team_score,
            outcome_point=snapshot.outcome_point,
            commence_time=snapshot.commence_time,
            graded_at=graded_at,
            created_at=created_at,
        )
