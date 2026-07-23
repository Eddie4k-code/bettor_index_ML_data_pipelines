"""Shared outcome resolution and win/loss/push helpers for team-bet grade builders."""

from schemas.games import CompletedGameRow
from schemas.grade import GradeOutcome
from schemas.snapshot import TeamBetSnapshotRecordBase


def names_match(left: str, right: str) -> bool:
    return left.strip().casefold() == right.strip().casefold()


def resolve_outcome_team_id(snapshot: TeamBetSnapshotRecordBase) -> int | None:
    if not snapshot.outcome_name:
        return None

    if names_match(snapshot.outcome_name, snapshot.home_team):
        return snapshot.home_team_id
    if names_match(snapshot.outcome_name, snapshot.away_team):
        return snapshot.away_team_id
    return None


def team_and_opponent_scores(
    game: CompletedGameRow,
    team_id: int,
) -> tuple[int, int] | None:
    if game.home_team_id == team_id:
        return game.home_team_score, game.away_team_score
    if game.away_team_id == team_id:
        return game.away_team_score, game.home_team_score
    return None


def grade_moneyline_outcome(team_score: int, opponent_score: int) -> GradeOutcome:
    if team_score > opponent_score:
        return "win"
    if team_score < opponent_score:
        return "loss"
    return "push"


def spread_margin(team_score: int, opponent_score: int, spread: float) -> float:
    return (team_score + spread) - opponent_score


def grade_spread_outcome(margin: float) -> GradeOutcome:
    if margin > 0:
        return "win"
    if margin < 0:
        return "loss"
    return "push"


def parse_direction(outcome_name: str) -> str | None:
    normalized = outcome_name.strip().casefold()
    if normalized in ("over", "under"):
        return normalized
    return None


def grade_totals_outcome(combined_total: int, line: float, direction: str) -> GradeOutcome:
    if combined_total == line:
        return "push"
    if direction == "over":
        return "win" if combined_total > line else "loss"
    return "win" if combined_total < line else "loss"
