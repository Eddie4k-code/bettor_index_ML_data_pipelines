"""Unit tests for upstream games model and games read repository."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine, inspect

from db.models.upstream.games import Game
from repositories.games_read_repository import GamesReadRepository
from schemas.games import COMPLETED_GAME_STATUSES, CompletedGameRow

COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)
GAME_DATE = datetime(2026, 7, 21, 23, 30, tzinfo=timezone.utc)


class TestUpstreamGameModel:
    def test_table_name_and_key_columns(self):
        engine = create_engine("sqlite:///:memory:")
        Game.__table__.create(engine)
        columns = {column["name"] for column in inspect(engine).get_columns("games")}

        assert "id" in columns
        assert "season" in columns
        assert "sport_key" in columns
        assert "home_team_id" in columns
        assert "away_team_id" in columns
        assert "home_team_score" in columns
        assert "away_team_score" in columns
        assert "status" in columns


class TestGamesReadRepository:
    def _completed_game_orm(self, **overrides) -> Game:
        defaults = {
            "id": 101,
            "season": 2026,
            "date": GAME_DATE,
            "status": "finished",
            "home_team": "boston celtics",
            "home_team_id": 1,
            "away_team": "los angeles lakers",
            "away_team_id": 2,
            "home_team_score": 112,
            "away_team_score": 105,
            "sport_key": "basketball_nba",
        }
        defaults.update(overrides)
        return Game(**defaults)

    def test_maps_completed_game_to_dto(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.order_by.return_value.first.return_value = (
            self._completed_game_orm()
        )

        row = GamesReadRepository(db).fetch_completed_game(
            sport_key="basketball_nba",
            event_id="evt-1",
            home_team_id=1,
            away_team_id=2,
            commence_time=COMMENCE_TIME,
        )

        assert row == CompletedGameRow(
            sport_key="basketball_nba",
            status="finished",
            home_team="boston celtics",
            away_team="los angeles lakers",
            home_team_id=1,
            away_team_id=2,
            home_team_score=112,
            away_team_score=105,
            date=GAME_DATE,
        )

    def test_returns_none_when_no_matching_game(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        row = GamesReadRepository(db).fetch_completed_game(
            sport_key="basketball_nba",
            event_id="evt-missing",
            home_team_id=1,
            away_team_id=2,
            commence_time=COMMENCE_TIME,
        )

        assert row is None

    @pytest.mark.parametrize("status", ["scheduled", "in_progress", "postponed"])
    def test_completed_statuses_constant_excludes_non_final_values(self, status):
        assert status not in COMPLETED_GAME_STATUSES

    @pytest.mark.parametrize("status", ["finished", "status_final", "final", "FINISHED"])
    def test_accepts_sport_specific_completed_statuses(self, status):
        db = MagicMock()
        db.query.return_value.filter.return_value.order_by.return_value.first.return_value = (
            self._completed_game_orm(status=status.lower() if status != "FINISHED" else status)
        )

        row = GamesReadRepository(db).fetch_completed_game(
            sport_key="basketball_nba",
            event_id="evt-1",
            home_team_id=1,
            away_team_id=2,
            commence_time=COMMENCE_TIME,
        )

        assert row is not None
        assert row.status == (status.lower() if status != "FINISHED" else status)
