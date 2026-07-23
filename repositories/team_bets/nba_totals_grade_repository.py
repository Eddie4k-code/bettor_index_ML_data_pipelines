"""Append-only writes to ``nba_team_bet_totals_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_totals_grades import NbaTeamBetTotalsGrade
from interfaces.nba_totals_grade_repository_interface import NbaTotalsGradeRepositoryInterface
from schemas.team_bets import NbaTotalsGradeRecord


class NbaTotalsGradeRepository(NbaTotalsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NbaTotalsGradeRecord) -> bool:
        existing = (
            self.db.query(NbaTeamBetTotalsGrade)
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

        self.db.add(NbaTeamBetTotalsGrade(**record.model_dump()))
        self.db.commit()
        return True
