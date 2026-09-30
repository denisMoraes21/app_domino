"""Domino piece domain entity."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DominoPiece:
    """
    Represents a domino piece (pedra) in the game.

    A domino piece has two sides, each with values from 0 to 6.
    Doubles (doubles/carocas) are pieces where both sides have the same value.
    """
    side_a: int
    side_b: int

    def __post_init__(self) -> None:
        """Validate piece values are within valid range."""
        if not (0 <= self.side_a <= 6):
            raise ValueError(f"side_a must be between 0 and 6, got {self.side_a}")
        if not (0 <= self.side_b <= 6):
            raise ValueError(f"side_b must be between 0 and 6, got {self.side_b}")

    @property
    def values(self) -> Tuple[int, int]:
        """Return the piece values as a tuple."""
        return (self.side_a, self.side_b)

    def is_double(self) -> bool:
        """Check if this is a double (caroca) piece."""
        return self.side_a == self.side_b

    def get_total_value(self) -> int:
        """Get the sum of both sides (used for double scoring)."""
        return self.side_a + self.side_b

    def has_value(self, value: int) -> bool:
        """Check if the piece has a specific value on either side."""
        return self.side_a == value or self.side_b == value

    def get_opposite_side(self, value: int) -> int:
        """
        Get the opposite side value when one side is known.

        Args:
            value: The value on one side of the piece

        Returns:
            The value on the other side

        Raises:
            ValueError: If the value is not on this piece
        """
        if self.side_a == value:
            return self.side_b
        elif self.side_b == value:
            return self.side_a
        else:
            raise ValueError(f"Value {value} not found on piece {self}")

    def __str__(self) -> str:
        """Return string representation like (6|6) or (3|5)."""
        return f"({self.side_a}|{self.side_b})"

    def __repr__(self) -> str:
        """Return detailed representation."""
        double_status = "double" if self.is_double() else "regular"
        return f"DominoPiece({self.side_a}, {self.side_b}) [{double_status}]"


def generate_full_set() -> list[DominoPiece]:
    """
    Generate a complete set of 28 domino pieces (0-0 to 6-6).

    Returns:
        List of all DominoPiece instances in a standard set
    """
    pieces = []
    for i in range(7):
        for j in range(i, 7):
            pieces.append(DominoPiece(i, j))
    return pieces
