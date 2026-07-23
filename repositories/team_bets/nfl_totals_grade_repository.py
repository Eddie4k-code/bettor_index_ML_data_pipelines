"""Append-only writes to ``nfl_team_bet_totals_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_totals_grades import NflTeamBetTotalsGrade
from interfaces.nfl_totals_grade_repository_interface import NflTotalsGradeRepositoryInterface
from schemas.team_bets import NflTotalsGradeRecord


class NflTotalsGradeRepository(NflTotalsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NflTotalsGradeRecord) -> bool:
        existing = (
            self.db.query(NflTeamBetTotalsGrade)
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

        self.db.add(NflTeamBetTotalsGrade(**record.model_dump()))
        self.db.commit()
        return True
