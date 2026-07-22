"""Shared validation helpers for team-bet snapshot builders."""

from datetime import datetime

from schemas.snapshot import ALLOWED_BOOKMAKERS
from schemas.team_bets.upstream_rows import FeaturedOddsRow, TeamBetHitRateRowBase


def join_keys_match(odds: FeaturedOddsRow, hit_rate: TeamBetHitRateRowBase) -> bool:
    return (
        odds.event_id == hit_rate.event_id
        and odds.bookmaker == hit_rate.bookmaker
        and odds.market_key == hit_rate.market_key
        and odds.outcome_name == hit_rate.outcome_name
    )


def is_pregame_pair(
    *,
    observation_time: datetime,
    odds: FeaturedOddsRow,
    hit_rate: TeamBetHitRateRowBase,
) -> bool:
    if odds.bookmaker not in ALLOWED_BOOKMAKERS:
        return False
    if odds.market_last_update > observation_time:
        return False
    if hit_rate.market_last_update > observation_time:
        return False
    if odds.commence_time <= observation_time:
        return False
    if not join_keys_match(odds, hit_rate):
        return False
    return True
