"""Sport-agnostic totals grade builder."""

from datetime import datetime
from typing import TypeVar

from builders.team_bets._grading import grade_totals_outcome, parse_direction
from interfaces.team_bet_grade_builder_interfaces import TotalsGradeBuilderInterface
from schemas.games import CompletedGameRow
from schemas.grade import TeamBetGradeRecordBase
from schemas.snapshot import TeamBetSnapshotRecordBase

TGradeRecord = TypeVar("TGradeRecord", bound=TeamBetGradeRecordBase)


class TotalsGradeBuilder(TotalsGradeBuilderInterface):
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

        direction = parse_direction(snapshot.outcome_name)
        if direction is None:
            return None

        combined_total = game.home_team_score + game.away_team_score
        grade_outcome = grade_totals_outcome(combined_total, snapshot.outcome_point, direction)

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
