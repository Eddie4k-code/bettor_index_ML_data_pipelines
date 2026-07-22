"""Sport-agnostic moneyline snapshot builder."""

from datetime import datetime
from typing import TypeVar

from builders.team_bets._validation import is_pregame_pair
from interfaces.team_bet_snapshot_builder_interfaces import H2hSnapshotBuilderInterface
from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.upstream_rows import FeaturedOddsRow, TeamBetH2hHitRateRow

TH2hRecord = TypeVar("TH2hRecord", bound=TeamBetSnapshotRecordBase)


class H2hSnapshotBuilder(H2hSnapshotBuilderInterface):
    def build(
        self,
        *,
        observation_time: datetime,
        odds: FeaturedOddsRow,
        hit_rate: TeamBetH2hHitRateRow,
        record_cls: type[TH2hRecord],
        created_at: datetime,
    ) -> TH2hRecord | None:
        if not is_pregame_pair(
            observation_time=observation_time,
            odds=odds,
            hit_rate=hit_rate,
        ):
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
            last_n_wins=hit_rate.last_n_wins,
            last_n_losses=hit_rate.last_n_losses,
            last_n_sample=hit_rate.last_n_sample,
            last_n_window=hit_rate.last_n_window,
            venue_wins=hit_rate.venue_wins,
            venue_losses=hit_rate.venue_losses,
            venue_sample=hit_rate.venue_sample,
            venue_window=hit_rate.venue_window,
            venue_type=hit_rate.venue_type,
            h2h_wins=hit_rate.h2h_wins,
            h2h_losses=hit_rate.h2h_losses,
            h2h_sample=hit_rate.h2h_sample,
            h2h_window=hit_rate.h2h_window,
        )
