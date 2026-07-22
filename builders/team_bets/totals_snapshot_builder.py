"""Sport-agnostic totals snapshot builder."""

from datetime import datetime
from typing import TypeVar

from builders.team_bets._validation import is_pregame_pair
from interfaces.team_bet_snapshot_builder_interfaces import TotalsSnapshotBuilderInterface
from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.upstream_rows import FeaturedOddsRow, TeamBetTotalsHitRateRow

TTotalsRecord = TypeVar("TTotalsRecord", bound=TeamBetSnapshotRecordBase)


class TotalsSnapshotBuilder(TotalsSnapshotBuilderInterface):
    def build(
        self,
        *,
        observation_time: datetime,
        odds: FeaturedOddsRow,
        hit_rate: TeamBetTotalsHitRateRow,
        record_cls: type[TTotalsRecord],
        created_at: datetime,
    ) -> TTotalsRecord | None:
        if not is_pregame_pair(
            observation_time=observation_time,
            odds=odds,
            hit_rate=hit_rate,
        ):
            return None
        if odds.outcome_point != hit_rate.line:
            return None
        if odds.outcome_name != hit_rate.direction:
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
            outcome_team_id=None,
            hit_rate_market_last_update=hit_rate.market_last_update,
            created_at=created_at,
            direction=hit_rate.direction,
            line=hit_rate.line,
            configured_window=hit_rate.configured_window,
            home_team_clears=hit_rate.home_team_clears,
            home_team_sample=hit_rate.home_team_sample,
            away_team_clears=hit_rate.away_team_clears,
            away_team_sample=hit_rate.away_team_sample,
            h2h_window=hit_rate.h2h_window,
            h2h_sample=hit_rate.h2h_sample,
            h2h_clears=hit_rate.h2h_clears,
            h2h_avg_total=hit_rate.h2h_avg_total,
        )
