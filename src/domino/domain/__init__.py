"""Domino Amazonense domain layer."""

from .piece import DominoPiece, generate_full_set
from .board import DominoBoard, EndType, BoardPosition
from .scorer import (
    ProgressiveScorer,
    HandCounter,
    BatidaCalculator,
    BloqueioCalculator,
    BatidaResult,
    BloqueioResult,
)
from .events import (
    DomainEvent,
    PiecePlayedEvent,
    ScoredEvent,
    GameEndedEvent,
    GamePhase,
    WinCondition,
    EventDispatcher,
)

__all__ = [
    # Pieces
    "DominoPiece",
    "generate_full_set",
    # Board
    "DominoBoard",
    "EndType",
    "BoardPosition",
    # Scoring
    "ProgressiveScorer",
    "HandCounter",
    "BatidaCalculator",
    "BloqueioCalculator",
    "BatidaResult",
    "BloqueioResult",
    # Events
    "DomainEvent",
    "PiecePlayedEvent",
    "ScoredEvent",
    "GameEndedEvent",
    "GamePhase",
    "WinCondition",
    "EventDispatcher",
]
