"""Append-only writes to ``nfl_team_bet_spreads_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_spreads_grades import NflTeamBetSpreadsGrade
from interfaces.nfl_spreads_grade_repository_interface import NflSpreadsGradeRepositoryInterface
from schemas.team_bets import NflSpreadsGradeRecord


class NflSpreadsGradeRepository(NflSpreadsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NflSpreadsGradeRecord) -> bool:
        existing = (
            self.db.query(NflTeamBetSpreadsGrade)
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

        self.db.add(NflTeamBetSpreadsGrade(**record.model_dump()))
        self.db.commit()
        return True
