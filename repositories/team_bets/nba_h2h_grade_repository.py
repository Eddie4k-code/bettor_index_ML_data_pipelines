"""Append-only writes to ``nba_team_bet_h2h_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_h2h_grades import NbaTeamBetH2hGrade
from interfaces.nba_h2h_grade_repository_interface import NbaH2hGradeRepositoryInterface
from schemas.team_bets import NbaH2hGradeRecord


class NbaH2hGradeRepository(NbaH2hGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NbaH2hGradeRecord) -> bool:
        existing = (
            self.db.query(NbaTeamBetH2hGrade)
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

        self.db.add(NbaTeamBetH2hGrade(**record.model_dump()))
        self.db.commit()
        return True
