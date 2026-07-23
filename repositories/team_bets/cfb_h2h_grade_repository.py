"""Append-only writes to ``cfb_team_bet_h2h_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_h2h_grades import CfbTeamBetH2hGrade
from interfaces.cfb_h2h_grade_repository_interface import CfbH2hGradeRepositoryInterface
from schemas.team_bets import CfbH2hGradeRecord


class CfbH2hGradeRepository(CfbH2hGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: CfbH2hGradeRecord) -> bool:
        existing = (
            self.db.query(CfbTeamBetH2hGrade)
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

        self.db.add(CfbTeamBetH2hGrade(**record.model_dump()))
        self.db.commit()
        return True
