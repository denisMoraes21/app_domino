"""Tests for DominoPiece domain entity."""

import pytest
from src.domino.domain.piece import DominoPiece, generate_full_set


class TestDominoPieceInit:
    """Tests for DominoPiece initialization and validation."""

    def test_valid_piece_creation(self):
        """Test creating a valid domino piece."""
        piece = DominoPiece(3, 5)
        assert piece.side_a == 3
        assert piece.side_b == 5

    def test_double_piece_creation(self):
        """Test creating a double (caroca) piece."""
        piece = DominoPiece(6, 6)
        assert piece.is_double() is True
        assert piece.get_total_value() == 12

    def test_zero_piece_creation(self):
        """Test creating a piece with zero (blank)."""
        piece = DominoPiece(0, 4)
        assert piece.side_a == 0
        assert piece.side_b == 4

    def test_invalid_side_a_too_low(self):
        """Test that side_a < 0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DominoPiece(-1, 3)
        assert "side_a must be between 0 and 6" in str(exc_info.value)

    def test_invalid_side_a_too_high(self):
        """Test that side_a > 6 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DominoPiece(7, 3)
        assert "side_a must be between 0 and 6" in str(exc_info.value)

    def test_invalid_side_b_too_high(self):
        """Test that side_b > 6 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DominoPiece(3, 8)
        assert "side_b must be between 0 and 6" in str(exc_info.value)


class TestDominoPieceProperties:
    """Tests for DominoPiece properties and methods."""

    def test_values_property(self):
        """Test the values property returns correct tuple."""
        piece = DominoPiece(2, 5)
        assert piece.values == (2, 5)

    def test_is_double_true(self):
        """Test is_double() returns True for doubles."""
        assert DominoPiece(0, 0).is_double() is True
        assert DominoPiece(3, 3).is_double() is True
        assert DominoPiece(6, 6).is_double() is True

    def test_is_double_false(self):
        """Test is_double() returns False for regular pieces."""
        assert DominoPiece(1, 2).is_double() is False
        assert DominoPiece(0, 6).is_double() is False

    def test_get_total_value_regular(self):
        """Test get_total_value() for regular pieces."""
        assert DominoPiece(2, 3).get_total_value() == 5
        assert DominoPiece(4, 5).get_total_value() == 9

    def test_get_total_value_double(self):
        """Test get_total_value() for doubles."""
        assert DominoPiece(0, 0).get_total_value() == 0
        assert DominoPiece(6, 6).get_total_value() == 12

    def test_has_value_positive(self):
        """Test has_value() returns True when value exists."""
        piece = DominoPiece(3, 5)
        assert piece.has_value(3) is True
        assert piece.has_value(5) is True

    def test_has_value_negative(self):
        """Test has_value() returns False when value doesn't exist."""
        piece = DominoPiece(3, 5)
        assert piece.has_value(0) is False
        assert piece.has_value(6) is False

    def test_get_opposite_side_a(self):
        """Test get_opposite_side() when matching side_a."""
        piece = DominoPiece(3, 7)
        assert piece.get_opposite_side(3) == 7

    def test_get_opposite_side_b(self):
        """Test get_opposite_side() when matching side_b."""
        piece = DominoPiece(3, 7)
        assert piece.get_opposite_side(7) == 3

    def test_get_opposite_side_not_found(self):
        """Test get_opposite_side() raises ValueError when value not found."""
        piece = DominoPiece(3, 7)
        with pytest.raises(ValueError) as exc_info:
            piece.get_opposite_side(5)
        assert "Value 5 not found on piece" in str(exc_info.value)


class TestDominoPieceStringRepresentation:
    """Tests for string representation."""

    def test_str_format(self):
        """Test string format is (a|b)."""
        assert str(DominoPiece(0, 0)) == "(0|0)"
        assert str(DominoPiece(3, 5)) == "(3|5)"
        assert str(DominoPiece(6, 6)) == "(6|6)"

    def test_repr_format(self):
        """Test repr format includes details."""
        piece = DominoPiece(6, 6)
        repr_str = repr(piece)
        assert "DominoPiece" in repr_str
        assert "6" in repr_str
        assert "double" in repr_str


class TestGenerateFullSet:
    """Tests for the generate_full_set function."""

    def test_set_size(self):
        """Test that full set has exactly 28 pieces."""
        pieces = generate_full_set()
        assert len(pieces) == 28

    def test_set_includes_all_doubles(self):
        """Test that all doubles (0-0 to 6-6) are included."""
        pieces = generate_full_set()
        doubles = [p for p in pieces if p.is_double()]
        assert len(doubles) == 7
        double_values = sorted([p.side_a for p in doubles])
        assert double_values == [0, 1, 2, 3, 4, 5, 6]

    def test_set_includes_zero_to_zero(self):
        """Test that (0|0) is in the set."""
        pieces = generate_full_set()
        has_zero_zero = any(p.side_a == 0 and p.side_b == 0 for p in pieces)
        assert has_zero_zero is True

    def test_set_includes_six_to_six(self):
        """Test that (6|6) is in the set."""
        pieces = generate_full_set()
        has_six_six = any(p.side_a == 6 and p.side_b == 6 for p in pieces)
        assert has_six_six is True

    def test_set_includes_all_combinations(self):
        """Test that all valid combinations are present exactly once."""
        pieces = generate_full_set()
        piece_pairs = [(p.side_a, p.side_b) for p in pieces]

        # Check no duplicates
        assert len(piece_pairs) == len(set(piece_pairs))

        # Check all combinations exist
        expected = set()
        for i in range(7):
            for j in range(i, 7):
                expected.add((i, j))

        assert set(piece_pairs) == expected


class TestDominoPieceImmutability:
    """Tests for piece immutability (frozen dataclass)."""

    def test_piece_is_immutable(self):
        """Test that piece attributes cannot be changed."""
        piece = DominoPiece(3, 5)
        with pytest.raises(Exception):  # Frozen instance error
            piece.side_a = 7
