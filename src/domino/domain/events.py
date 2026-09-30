"""Domain events for domino game state changes."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod


class GamePhase(Enum):
    """Current phase of the domino game."""
    OPENING = "opening"           # First piece (caroca) placed
    EXPANDING = "expanding"       # Main ends expanding
    BRANCHING = "branching"       # Lateral branches available
    BLOCKED = "blocked"           # No valid moves available
    ENDED = "ended"               # Game complete


class WinCondition(Enum):
    """How the game ended."""
    BATIDA = "batida"             # Player played all pieces
    BLOQUEIO = "bloqueio"         # Game blocked (no moves)
    TEMPO = "tempo"               # Time limit exceeded


@dataclass
class DomainEvent(ABC):
    """Base class for domain events."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert event to dictionary for serialization."""
        pass


@dataclass
class PiecePlayedEvent(DomainEvent):
    """Event fired when a piece is played."""
    player_id: str
    piece_str: str
    end_type: str
    board_ends: dict

    def to_dict(self) -> dict:
        return {
            "type": "piece_played",
            "player_id": self.player_id,
            "piece": self.piece_str,
            "end_type": self.end_type,
            "board_ends": self.board_ends,
        }


@dataclass
class ScoredEvent(DomainEvent):
    """Event fired when points are scored."""
    player_id: str
    points: int
    ends_sum: int
    multiplier: int
    stage: str
    phase: str

    def to_dict(self) -> dict:
        return {
            "type": "scored",
            "player_id": self.player_id,
            "points": self.points,
            "ends_sum": self.ends_sum,
            "multiplier": self.multiplier,
            "stage": self.stage,
            "phase": self.phase,
        }


@dataclass
class GameEndedEvent(DomainEvent):
    """Event fired when the game ends."""
    winner_id: str
    win_condition: str
    scores: dict

    def to_dict(self) -> dict:
        return {
            "type": "game_ended",
            "winner_id": self.winner_id,
            "win_condition": self.win_condition,
            "scores": self.scores,
        }


class EventDispatcher:
    """Simple event dispatcher for domain events."""

    def __init__(self):
        self._subscribers: dict[type, list[callable]] = {}

    def subscribe(self, event_type: type, handler: callable) -> None:
        """Subscribe a handler to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch an event to all subscribed handlers."""
        handlers = self._subscribers.get(type(event), [])
        for handler in handlers:
            handler(event)
