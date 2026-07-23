"""Point-in-time reads from the shared ``games`` table for post-game grading."""

from datetime import datetime, timedelta

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from db.models.upstream.games import Game
from interfaces.games_read_repository_interface import GamesReadRepositoryInterface
from schemas.games import COMPLETED_GAME_STATUSES, CompletedGameRow


class GamesReadRepository(GamesReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_completed_game(
        self,
        *,
        sport_key: str,
        event_id: str,
        home_team_id: int,
        away_team_id: int,
        commence_time: datetime,
    ) -> CompletedGameRow | None:
        del event_id  # Odds API event ids are not stored on ``games``; matchup keys resolve the row.

        window_start = commence_time - timedelta(days=1)
        window_end = commence_time + timedelta(days=1)

        row = (
            self.db.query(Game)
            .filter(
                Game.sport_key == sport_key,
                func.lower(Game.status).in_(COMPLETED_GAME_STATUSES),
                or_(
                    and_(Game.home_team_id == home_team_id, Game.away_team_id == away_team_id),
                    and_(Game.home_team_id == away_team_id, Game.away_team_id == home_team_id),
                ),
                Game.date >= window_start,
                Game.date <= window_end,
            )
            .order_by(func.abs(Game.date - commence_time))
            .first()
        )
        if row is None:
            return None

        return CompletedGameRow(
            sport_key=row.sport_key,
            status=row.status,
            home_team=row.home_team,
            away_team=row.away_team,
            home_team_id=row.home_team_id,
            away_team_id=row.away_team_id,
            home_team_score=row.home_team_score,
            away_team_score=row.away_team_score,
            date=row.date,
        )
