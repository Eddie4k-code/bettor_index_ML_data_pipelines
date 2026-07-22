"""ABC contracts for snapshot pipeline boundaries."""

from interfaces.team_bet_snapshot_builder_interfaces import (
    H2hSnapshotBuilderInterface,
    SpreadsSnapshotBuilderInterface,
    TotalsSnapshotBuilderInterface,
)

__all__ = [
    "H2hSnapshotBuilderInterface",
    "SpreadsSnapshotBuilderInterface",
    "TotalsSnapshotBuilderInterface",
]
