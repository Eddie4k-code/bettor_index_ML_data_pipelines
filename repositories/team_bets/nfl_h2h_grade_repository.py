"""Append-only writes to ``nfl_team_bet_h2h_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_h2h_grades import NflTeamBetH2hGrade
from interfaces.nfl_h2h_grade_repository_interface import NflH2hGradeRepositoryInterface
from schemas.team_bets import NflH2hGradeRecord


class NflH2hGradeRepository(NflH2hGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NflH2hGradeRecord) -> bool:
        existing = (
            self.db.query(NflTeamBetH2hGrade)
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

        self.db.add(NflTeamBetH2hGrade(**record.model_dump()))
        self.db.commit()
        return True
