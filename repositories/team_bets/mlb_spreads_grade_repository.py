"""Append-only writes to ``mlb_team_bet_spreads_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_spreads_grades import MlbTeamBetSpreadsGrade
from interfaces.mlb_spreads_grade_repository_interface import MlbSpreadsGradeRepositoryInterface
from schemas.team_bets import MlbSpreadsGradeRecord


class MlbSpreadsGradeRepository(MlbSpreadsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: MlbSpreadsGradeRecord) -> bool:
        existing = (
            self.db.query(MlbTeamBetSpreadsGrade)
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

        self.db.add(MlbTeamBetSpreadsGrade(**record.model_dump()))
        self.db.commit()
        return True
