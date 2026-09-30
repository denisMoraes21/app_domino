"""Progressive scoring logic for Domino Amazonense."""

from typing import Optional
from dataclasses import dataclass

from .piece import DominoPiece
from .board import DominoBoard, EndType
from .events import ScoredEvent, GamePhase


class ProgressiveScorer:
    """
    Handles progressive 4-ends scoring for Domino Amazonense.

    Scoring Rules:
    - Points only awarded when sum of all ends is a multiple of 5
    - Unfilled ends count as 0 for sum calculation
    - Progressive multipliers based on number of filled ends:
        * 1 end filled: 1x multiplier (Caroca + ponta)
        * 2 ends filled: 2x multiplier (4 pontas system begins)
        * 4 ends filled: 4x multiplier (full 4 pontas)
    - Base points = sum // 5
    - Final points = base_points * multiplier
    """

    POINTS_DIVISOR = 5
    VALID_MULTIPLIERS = {1, 2, 4}

    MULTIPLIER_MAP = {
        1: 1,
        2: 2,
        4: 4,
    }

    STAGE_NAMES = {
        1: "Caroca única",
        2: "Caroca + Ponta",
        4: "4 Pontas",
    }

    def calculate(self, board: DominoBoard, player_id: str) -> Optional[ScoredEvent]:
        """
        Calculate score for current board state.

        Args:
            board: The current game board
            player_id: ID of the player who just moved

        Returns:
            ScoredEvent if points were scored, None otherwise
        """
        ends_values = board.get_current_ends()
        filled_count = board.get_filled_ends_count()

        # No score possible with empty board
        if filled_count == 0:
            return None

        # Calculate sum (unfilled ends = 0)
        total_sum = sum(ends_values.values())

        # Must be multiple of 5 to score
        if total_sum % self.POINTS_DIVISOR != 0:
            return None

        # Calculate base points
        base_points = total_sum // self.POINTS_DIVISOR

        # Get progressive multiplier
        multiplier = self._get_multiplier(filled_count)
        final_points = base_points * multiplier

        # Determine game phase
        phase = self._get_phase(board)

        # Create score event
        event = ScoredEvent(
            player_id=player_id,
            points=final_points,
            ends_sum=total_sum,
            multiplier=multiplier,
            stage=self._get_stage_name(filled_count),
            phase=phase.value,
        )

        return event

    def _get_multiplier(self, filled_count: int) -> int:
        """
        Get the progressive multiplier based on filled end count.

        Args:
            filled_count: Number of ends currently filled (1-4)

        Returns:
            Multiplier value (1, 2, or 4)
        """
        return self.MULTIPLIER_MAP.get(filled_count, 1)

    def _get_stage_name(self, filled_count: int) -> str:
        """
        Get human-readable stage name.

        Args:
            filled_count: Number of ends currently filled

        Returns:
            Stage name string
        """
        return self.STAGE_NAMES.get(filled_count, f"{filled_count} pontas")

    def _get_phase(self, board: DominoBoard) -> GamePhase:
        """
        Determine current game phase based on board state.

        Args:
            board: The current game board

        Returns:
            Current GamePhase
        """
        if board.lateral_unlocked and board.get_filled_ends_count() >= 3:
            return GamePhase.BRANCHING
        elif board.get_filled_ends_count() >= 2:
            return GamePhase.EXPANDING
        elif board.get_filled_ends_count() == 1:
            return GamePhase.OPENING
        return GamePhase.BLOCKED

    def get_progression_info(self, board: DominoBoard) -> dict:
        """
        Get detailed information about current scoring progression.

        Args:
            board: The current game board

        Returns:
            Dictionary with progression details
        """
        ends = board.get_current_ends()
        filled = board.get_filled_ends_count()
        total = sum(ends.values())

        return {
            "ends_values": ends,
            "filled_count": filled,
            "total_sum": total,
            "can_score": total % self.POINTS_DIVISOR == 0 and filled > 0,
            "potential_points": (total // self.POINTS_DIVISOR) * self._get_multiplier(filled) if total % self.POINTS_DIVISOR == 0 else 0,
            "multiplier": self._get_multiplier(filled),
            "stage": self._get_stage_name(filled),
            "lateral_available": board.lateral_unlocked,
        }


class HandCounter:
    """Utility for counting points in player hands."""

    @staticmethod
    def count_pieces(pieces: list[DominoPiece]) -> int:
        """Count number of pieces in hand."""
        return len(pieces)

    @staticmethod
    def count_points(pieces: list[DominoPiece]) -> int:
        """
        Count total points (pontos) in a player's hand.

        Args:
            pieces: List of DominoPiece in hand

        Returns:
            Sum of all piece values
        """
        return sum(piece.get_total_value() for piece in pieces)

    @staticmethod
    def count_double_points(pieces: list[DominoPiece]) -> int:
        """
        Count points specifically from double pieces.

        Args:
            pieces: List of DominoPiece in hand

        Returns:
            Sum of double piece values
        """
        return sum(piece.get_total_value() for piece in pieces if piece.is_double())


@dataclass
class BatidaResult:
    """Result of a batida (empty hand) game end."""
    winner_id: str
    winner_hand: list[DominoPiece]
    loser_hands: dict[str, list[DominoPiece]]
    points_awarded: int


class BatidaCalculator:
    """Calculate batida (empty hand) game end scores."""

    def __init__(self, hand_counter: HandCounter | None = None):
        self.hand_counter = hand_counter or HandCounter()

    def calculate(self, winner_id: str, players: dict[str, list[DominoPiece]]) -> BatidaResult:
        """
        Calculate points awarded in a batida situation.

        In batida, the winner gets the sum of all opponents' hand points.

        Args:
            winner_id: ID of the player who went out
            players: Dictionary mapping player IDs to their remaining hands

        Returns:
            BatidaResult with scoring details
        """
        loser_hands = {
            pid: pieces for pid, pieces in players.items() if pid != winner_id
        }

        total_points = sum(
            self.hand_counter.count_points(pieces)
            for pieces in loser_hands.values()
        )

        return BatidaResult(
            winner_id=winner_id,
            winner_hand=players[winner_id],
            loser_hands=loser_hands,
            points_awarded=total_points,
        )


@dataclass
class BloqueioResult:
    """Result of a bloqueio (blocked game) end."""
    winner_id: str
    scores: dict[str, int]
    reason: str = "Fewest points in hand"


class BloqueioCalculator:
    """Calculate bloqueio (blocked game) end scores."""

    def __init__(self, hand_counter: HandCounter | None = None):
        self.hand_counter = hand_counter or HandCounter()

    def determine_winner(self, players: dict[str, list[DominoPiece]],
                        last_mover: Optional[str] = None) -> BloqueioResult:
        """
        Determine winner in a blocked game.

        Winner is the player with fewest points in hand.
        Tie-breaker: last player to move loses.

        Args:
            players: Dictionary mapping player IDs to their hands
            last_mover: Optional ID of last player who moved (for tie-breaker)

        Returns:
            BloqueioResult with winner and scores
        """
        hand_scores = {
            pid: self.hand_counter.count_points(pieces)
            for pid, pieces in players.items()
        }

        # Find minimum score
        min_score = min(hand_scores.values())
        candidates = [
            pid for pid, score in hand_scores.items()
            if score == min_score
        ]

        if len(candidates) == 1:
            winner_id = candidates[0]
            reason = "Fewest points in hand"
        else:
            # Tie-breaker
            if last_mover and last_mover in candidates:
                candidates.remove(last_mover)
            winner_id = candidates[0] if candidates else list(players.keys())[0]
            reason = "Tie-breaker: not last mover" if len(candidates) > 1 else "Fewest points in hand"

        return BloqueioResult(
            winner_id=winner_id,
            scores=hand_scores,
            reason=reason,
        )
