"""Append-only writes to ``cfb_team_bet_totals_grades``."""

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_totals_grades import CfbTeamBetTotalsGrade
from interfaces.cfb_totals_grade_repository_interface import CfbTotalsGradeRepositoryInterface
from schemas.team_bets import CfbTotalsGradeRecord


class CfbTotalsGradeRepository(CfbTotalsGradeRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: CfbTotalsGradeRecord) -> bool:
        existing = (
            self.db.query(CfbTeamBetTotalsGrade)
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

        self.db.add(CfbTeamBetTotalsGrade(**record.model_dump()))
        self.db.commit()
        return True
