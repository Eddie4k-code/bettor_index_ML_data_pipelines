"""Sport-agnostic spread snapshot builder."""

from datetime import datetime
from typing import TypeVar

from builders.team_bets._validation import is_pregame_pair
from interfaces.team_bet_snapshot_builder_interfaces import SpreadsSnapshotBuilderInterface
from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.upstream_rows import FeaturedOddsRow, TeamBetSpreadsHitRateRow

TSpreadsRecord = TypeVar("TSpreadsRecord", bound=TeamBetSnapshotRecordBase)


class SpreadsSnapshotBuilder(SpreadsSnapshotBuilderInterface):
    def build(
        self,
        *,
        observation_time: datetime,
        odds: FeaturedOddsRow,
        hit_rate: TeamBetSpreadsHitRateRow,
        record_cls: type[TSpreadsRecord],
        created_at: datetime,
    ) -> TSpreadsRecord | None:
        if not is_pregame_pair(
            observation_time=observation_time,
            odds=odds,
            hit_rate=hit_rate,
        ):
            return None
        if odds.outcome_point != hit_rate.spread:
            return None

        return record_cls(
            observation_time=observation_time,
            event_id=odds.event_id,
            bookmaker=odds.bookmaker,
            outcome_name=odds.outcome_name,
            commence_time=odds.commence_time,
            outcome_point=odds.outcome_point,
            outcome_price=odds.outcome_price,
            market_last_update=odds.market_last_update,
            home_team=odds.home_team,
            away_team=odds.away_team,
            home_team_id=odds.home_team_id,
            away_team_id=odds.away_team_id,
            outcome_team_id=hit_rate.outcome_team_id,
            hit_rate_market_last_update=hit_rate.market_last_update,
            created_at=created_at,
            spread=hit_rate.spread,
            last_n_covers=hit_rate.last_n_covers,
            last_n_sample=hit_rate.last_n_sample,
            last_n_window=hit_rate.last_n_window,
            h2h_covers=hit_rate.h2h_covers,
            h2h_sample=hit_rate.h2h_sample,
            h2h_window=hit_rate.h2h_window,
            venue_covers=hit_rate.venue_covers,
            venue_sample=hit_rate.venue_sample,
            venue_window=hit_rate.venue_window,
            venue_type=hit_rate.venue_type,
        )
