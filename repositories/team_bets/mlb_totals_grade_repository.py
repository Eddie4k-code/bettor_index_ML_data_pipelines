"""Append-only writes to ``mlb_team_bet_totals_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_totals_grades import MlbTeamBetTotalsGrade
from interfaces.mlb_totals_grade_repository_interface import MlbTotalsGradeRepositoryInterface
from schemas.team_bets import MlbTotalsGradeRecord


class MlbTotalsGradeRepository(MlbTotalsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: MlbTotalsGradeRecord) -> bool:
        existing = (
            self.db.query(MlbTeamBetTotalsGrade)
            .filter_by(
                observation_time=record.observation_time,
                event_id=record.event_id,
                bookmaker=record.bookmaker,
                outcome_name=record.outcome_name,
                snapshot_version=record.snapshot_version,
            )
            .first()
        )
        if existing is not None:
            return False

        self.db.add(MlbTeamBetTotalsGrade(**record.model_dump()))
        self.db.commit()
        return True
