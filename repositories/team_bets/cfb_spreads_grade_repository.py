"""Append-only writes to ``cfb_team_bet_spreads_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_spreads_grades import CfbTeamBetSpreadsGrade
from interfaces.cfb_spreads_grade_repository_interface import CfbSpreadsGradeRepositoryInterface
from schemas.team_bets import CfbSpreadsGradeRecord


class CfbSpreadsGradeRepository(CfbSpreadsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: CfbSpreadsGradeRecord) -> bool:
        existing = (
            self.db.query(CfbTeamBetSpreadsGrade)
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

        self.db.add(CfbTeamBetSpreadsGrade(**record.model_dump()))
        self.db.commit()
        return True
