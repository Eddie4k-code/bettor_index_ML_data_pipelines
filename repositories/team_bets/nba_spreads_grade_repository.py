"""Append-only writes to ``nba_team_bet_spreads_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_spreads_grades import NbaTeamBetSpreadsGrade
from interfaces.nba_spreads_grade_repository_interface import NbaSpreadsGradeRepositoryInterface
from schemas.team_bets import NbaSpreadsGradeRecord


class NbaSpreadsGradeRepository(NbaSpreadsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NbaSpreadsGradeRecord) -> bool:
        existing = (
            self.db.query(NbaTeamBetSpreadsGrade)
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

        self.db.add(NbaTeamBetSpreadsGrade(**record.model_dump()))
        self.db.commit()
        return True
