"""Read-only mirror of revised_engine ``games`` table."""

from sqlalchemy import Column, DateTime, Integer, String

from db.models.base import UpstreamBase


class Game(UpstreamBase):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False, primary_key=True)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    home_team = Column(String, nullable=False, primary_key=True)
    home_team_id = Column(Integer, nullable=False, primary_key=True)
    away_team = Column(String, nullable=False, primary_key=True)
    away_team_id = Column(Integer, nullable=False, primary_key=True)
    home_team_score = Column(Integer, nullable=False)
    away_team_score = Column(Integer, nullable=False)
    sport_key = Column(String, nullable=False, primary_key=True)
