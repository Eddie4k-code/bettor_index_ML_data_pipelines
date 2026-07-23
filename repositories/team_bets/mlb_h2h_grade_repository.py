"""Append-only writes to ``mlb_team_bet_h2h_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_h2h_grades import MlbTeamBetH2hGrade
from interfaces.mlb_h2h_grade_repository_interface import MlbH2hGradeRepositoryInterface
from schemas.team_bets import MlbH2hGradeRecord


class MlbH2hGradeRepository(MlbH2hGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: MlbH2hGradeRecord) -> bool:
        existing = (
            self.db.query(MlbTeamBetH2hGrade)
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

        self.db.add(MlbTeamBetH2hGrade(**record.model_dump()))
        self.db.commit()
        return True
