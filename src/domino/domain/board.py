"""Domino board domain model with progressive 4-ends system."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict, Literal


class EndType(Enum):
    """
    Types of ends on the domino board for progressive scoring.

    The board progresses through stages:
    1. Start: Single caroca piece
    2. Main ends: Left and right expansion
    3. Lateral branches: Top/bottom (unlocked after both main ends filled)
    """
    MAIN_LEFT = auto()      # Primary left end
    MAIN_RIGHT = auto()     # Primary right end
    LATERAL_TOP = auto()    # Branch top (unlocked after 2 main ends)
    LATERAL_BOTTOM = auto() # Branch bottom (unlocked after 2 main ends)


@dataclass(frozen=True)
class BoardPosition:
    """
    Represents a piece's position on the board.

    Attributes:
        piece: The domino piece placed at this position
        orientation: 'longitudinal' for regular pieces, 'transversal' for doubles
        connected_to: The end type this piece extends from (None for starting piece)
    """
    piece: 'DominoPiece'  # type: ignore[name-defined]
    orientation: Literal['longitudinal', 'transversal'] = 'longitudinal'
    connected_to: Optional[EndType] = None

    @property
    def free_side_value(self) -> int:
        """
        Get the value at the free (outer) end of this piece.

        For longitudinal pieces: returns side_b
        For transversal pieces (doubles): returns sum of both sides
        """
        if self.orientation == 'transversal':
            return self.piece.get_total_value()
        return self.piece.side_b

    def __str__(self) -> str:
        orientation_symbol = "⟂" if self.orientation == "transversal" else "—"
        return f"{orientation_symbol}{self.piece}"


@dataclass
class DominoBoard:
    """
    Graph-based board representation for progressive 4-ends domino system.

    Board structure:
           [Lateral Top]
                  |
        [Left Main] --- [Caroca] --- [Right Main]
                  |
           [Lateral Bottom]

    The board supports:
    - Single caroca start
    - Two main ends that expand (left and right)
    - Conditional lateral branches (top and bottom, unlocked after both main ends filled)
    - Progressive scoring with unfilled ends counting as 0
    """

    # Position tracker for each end type
    positions: Dict[EndType, Optional[BoardPosition]] = field(default_factory=lambda: {
        EndType.MAIN_LEFT: None,
        EndType.MAIN_RIGHT: None,
        EndType.LATERAL_TOP: None,
        EndType.LATERAL_BOTTOM: None,
    })

    # Track starting caroca piece
    caroca: Optional[BoardPosition] = None

    # Board state flags
    lateral_unlocked: bool = False
    game_started: bool = False

    def add_starting_piece(self, piece: 'DominoPiece') -> None:  # type: ignore[name-defined]
        """
        Place the starting caroca piece.

        Args:
            piece: The starting domino piece (typically a double)

        Raises:
            ValueError: If game has already started or piece is invalid
        """
        if self.game_started:
            raise ValueError("Board already has a starting piece")

        # For starting piece, use transversal orientation if it's a double
        orientation = 'transversal' if piece.is_double() else 'longitudinal'

        self.caroca = BoardPosition(piece=piece, orientation=orientation)
        self.positions[EndType.MAIN_LEFT] = BoardPosition(piece=piece, orientation=orientation)
        self.positions[EndType.MAIN_RIGHT] = BoardPosition(piece=piece, orientation=orientation)
        self.game_started = True

    def add_piece(self, piece: 'DominoPiece', to_end: EndType,  # type: ignore[name-defined]
                  connect_side: Literal[0, 1]) -> BoardPosition:
        """
        Add a piece to a specific end of the board.

        Args:
            piece: The domino piece to place
            to_end: Which end to attach to
            connect_side: Which side of the piece connects (0=side_a, 1=side_b)

        Returns:
            The new BoardPosition created

        Raises:
            ValueError: If the move is invalid (wrong connection, lateral locked, etc.)
        """
        if not self.game_started:
            raise ValueError("Game must start with a caroca piece")

        # Validate lateral branch access
        if to_end in (EndType.LATERAL_TOP, EndType.LATERAL_BOTTOM):
            if not self.lateral_unlocked:
                raise ValueError(
                    "Lateral branches only available after both main ends are filled"
                )

        # Get current end position to match
        current_end = self.positions[to_end]
        if current_end is None:
            raise ValueError(f"No piece at {to_end} to connect to")

        # Validate connection value
        connect_value = piece.side_a if connect_side == 0 else piece.side_b
        target_value = current_end.free_side_value

        if connect_value != target_value:
            raise ValueError(
                f"Cannot connect {piece} to {to_end}: "
                f"piece side {connect_value} doesn't match target {target_value}"
            )

        # Determine orientation
        is_double = piece.is_double()
        connected_value = connect_value
        opposite_value = piece.side_b if connect_side == 0 else piece.side_a

        if is_double:
            orientation: Literal['longitudinal', 'transversal'] = 'transversal'
        else:
            orientation = 'longitudinal'

        # Create new position
        new_position = BoardPosition(
            piece=piece,
            orientation=orientation,
            connected_to=to_end
        )

        # Update board state
        self.positions[to_end] = new_position

        # Check if lateral branches should unlock
        self._check_lateral_unlock()

        return new_position

    def get_current_ends(self) -> Dict[EndType, int]:
        """
        Get current values at each end.

        Returns:
            Dictionary mapping EndType to value (0 for unfilled ends)

        Note:
            Unfilled ends return 0 for scoring calculation purposes.
        """
        result = {}
        for end_type, position in self.positions.items():
            if position is None:
                result[end_type] = 0
            else:
                result[end_type] = position.free_side_value
        return result

    def get_filled_ends_count(self) -> int:
        """Count how many ends currently have pieces placed."""
        return sum(1 for pos in self.positions.values() if pos is not None)

    def is_valid_move(self, piece: 'DominoPiece', to_end: EndType) -> bool:  # type: ignore[name-defined]
        """
        Check if a piece can be legally played at a specific end.

        Args:
            piece: The domino piece to check
            to_end: The end type to check

        Returns:
            True if the move is valid, False otherwise
        """
        # Lateral branches check
        if to_end in (EndType.LATERAL_TOP, EndType.LATERAL_BOTTOM):
            if not self.lateral_unlocked:
                return False

        # Get current end value
        current_end = self.positions[to_end]
        if current_end is None:
            return False

        target_value = current_end.free_side_value

        # Check if piece has matching value
        return piece.has_value(target_value)

    def get_valid_moves(self, piece: 'DominoPiece') -> list[EndType]:  # type: ignore[name-defined]
        """
        Get all ends where a piece can be legally played.

        Args:
            piece: The domino piece to check

        Returns:
            List of EndType values where the piece can be played
        """
        valid_moves = []
        for end_type in EndType:
            if self.is_valid_move(piece, end_type):
                valid_moves.append(end_type)
        return valid_moves

    def _check_lateral_unlock(self) -> None:
        """Unlock lateral branches when both main ends are filled."""
        left_filled = self.positions[EndType.MAIN_LEFT] is not None
        right_filled = self.positions[EndType.MAIN_RIGHT] is not None
        self.lateral_unlocked = left_filled and right_filled

    def is_complete(self) -> bool:
        """Check if all four ends are filled."""
        return all(pos is not None for pos in self.positions.values())

    def __str__(self) -> str:
        """Return a text representation of the board."""
        ends = self.get_current_ends()
        filled = self.get_filled_ends_count()
        return (
            f"DominoBoard(filled_ends={filled}/4, "
            f"lateral_unlocked={self.lateral_unlocked}, "
            f"ends={ends})"
        )
