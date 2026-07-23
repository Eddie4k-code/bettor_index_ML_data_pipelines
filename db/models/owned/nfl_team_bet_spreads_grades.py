"""Owned NFL team bet spreads grade table."""

from sqlalchemy import Column, DateTime, Float, Integer, String

from db.models.base import Base


class NflTeamBetSpreadsGrade(Base):
    __tablename__ = "nfl_team_bet_spreads_grades"

    observation_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    event_id = Column(String, primary_key=True, nullable=False)
    bookmaker = Column(String, primary_key=True, nullable=False)
    outcome_name = Column(String, primary_key=True, nullable=False)
    snapshot_version = Column(String, primary_key=True, nullable=False)
    sport_key = Column(String, nullable=False, index=True)
    market_key = Column(String, nullable=False, index=True)
    grade_outcome = Column(String, nullable=False)
    grade_version = Column(String, nullable=False)
    home_team_score = Column(Integer, nullable=True)
    away_team_score = Column(Integer, nullable=True)
    outcome_point = Column(Float, nullable=True)
    commence_time = Column(DateTime(timezone=True), nullable=False)
    graded_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
