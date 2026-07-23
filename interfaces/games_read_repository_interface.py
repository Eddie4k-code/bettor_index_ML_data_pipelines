"""ABC for read-only completed game lookups used by grade pipelines."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.games import CompletedGameRow


class GamesReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_completed_game(
        self,
        *,
        sport_key: str,
        event_id: str,
        home_team_id: int,
        away_team_id: int,
        commence_time: datetime,
    ) -> CompletedGameRow | None:
        """Return final scores for the completed game matching the snapshot event."""
