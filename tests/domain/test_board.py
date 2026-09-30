"""Tests for DominoBoard domain model."""

import pytest
from src.domino.domain.piece import DominoPiece
from src.domino.domain.board import DominoBoard, EndType, BoardPosition


class TestBoardInitialization:
    """Tests for board initialization."""

    def test_new_board_empty(self):
        """Test that a new board starts empty."""
        board = DominoBoard()
        assert board.game_started is False
        assert board.lateral_unlocked is False
        assert board.caroca is None

    def test_new_board_ends_zero(self):
        """Test that new board ends return 0."""
        board = DominoBoard()
        ends = board.get_current_ends()
        assert all(value == 0 for value in ends.values())

    def test_new_board_filled_count_zero(self):
        """Test that new board has 0 filled ends."""
        board = DominoBoard()
        assert board.get_filled_ends_count() == 0


class TestStartingPiece:
    """Tests for starting caroca piece."""

    def test_add_starting_piece_caroca(self):
        """Test adding a double (caroca) as starting piece."""
        board = DominoBoard()
        caroca = DominoPiece(6, 6)
        board.add_starting_piece(caroca)

        assert board.game_started is True
        assert board.caroca is not None
        assert board.caroca.piece == caroca
        assert board.caroca.orientation == "transversal"

    def test_add_starting_piece_sets_both_main_ends(self):
        """Test that starting piece sets both main left and right ends."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))

        assert board.positions[EndType.MAIN_LEFT] is not None
        assert board.positions[EndType.MAIN_RIGHT] is not None

    def test_add_starting_piece_regular_piece(self):
        """Test adding a non-double as starting piece."""
        board = DominoBoard()
        piece = DominoPiece(3, 5)
        board.add_starting_piece(piece)

        assert board.caroca.orientation == "longitudinal"

    def test_cannot_add_second_starting_piece(self):
        """Test that adding another starting piece raises ValueError."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))

        with pytest.raises(ValueError) as exc_info:
            board.add_starting_piece(DominoPiece(5, 5))
        assert "already has a starting piece" in str(exc_info.value)


class TestBoardMoves:
    """Tests for adding pieces to the board."""

    @pytest.fixture
    def board_with_caroca(self):
        """Fixture providing a board with starting piece."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))
        return board

    def test_add_piece_to_main_right(self, board_with_caroca):
        """Test adding a piece to main right end."""
        piece = DominoPiece(6, 4)
        position = board_with_caroca.add_piece(piece, EndType.MAIN_RIGHT, connect_side=0)

        assert position.piece == piece
        assert board_with_caroca.positions[EndType.MAIN_RIGHT].piece == piece
        assert board_with_caroca.get_filled_ends_count() == 2

    def test_add_piece_to_main_left(self, board_with_caroca):
        """Test adding a piece to main left end."""
        piece = DominoPiece(6, 2)
        position = board_with_caroca.add_piece(piece, EndType.MAIN_LEFT, connect_side=1)

        assert position.piece == piece
        assert board_with_caroca.get_filled_ends_count() == 2

    def test_add_piece_invalid_connection(self, board_with_caroca):
        """Test that invalid connection value raises ValueError."""
        piece = DominoPiece(3, 4)  # Doesn't have 6
        with pytest.raises(ValueError) as exc_info:
            board_with_caroca.add_piece(piece, EndType.MAIN_RIGHT, connect_side=0)
        assert "doesn't match target" in str(exc_info.value)

    def test_add_piece_wrong_side(self, board_with_caroca):
        """Test adding piece with correct value on wrong side."""
        piece = DominoPiece(4, 6)  # Has 6 on side_b
        # Try to connect with side_a (4)
        with pytest.raises(ValueError) as exc_info:
            board_with_caroca.add_piece(piece, EndType.MAIN_RIGHT, connect_side=0)
        assert "doesn't match target" in str(exc_info.value)

    def test_add_piece_correct_side_b(self, board_with_caroca):
        """Test adding piece using side_b for connection."""
        piece = DominoPiece(4, 6)  # Has 6 on side_b
        position = board_with_caroca.add_piece(piece, EndType.MAIN_RIGHT, connect_side=1)

        assert position.piece == piece
        assert board_with_caroca.get_filled_ends_count() == 2

    def test_double_orientation_transversal(self, board_with_caroca):
        """Test that double pieces get transversal orientation."""
        piece = DominoPiece(6, 6)
        position = board_with_caroca.add_piece(piece, EndType.MAIN_RIGHT, connect_side=0)

        assert position.orientation == "transversal"

    def test_regular_piece_orientation_longitudinal(self, board_with_caroca):
        """Test that regular pieces get longitudinal orientation."""
        piece = DominoPiece(6, 4)
        position = board_with_caroca.add_piece(piece, EndType.MAIN_RIGHT, connect_side=0)

        assert position.orientation == "longitudinal"


class TestLateralBranches:
    """Tests for lateral branch unlocking."""

    @pytest.fixture
    def board_with_both_main_ends(self):
        """Fixture with both main ends filled."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))

        # Fill main right
        board.add_piece(DominoPiece(6, 4), EndType.MAIN_RIGHT, connect_side=0)

        # Fill main left
        board.add_piece(DominoPiece(6, 2), EndType.MAIN_LEFT, connect_side=1)

        return board

    def test_lateral_unlocked_after_both_main_ends(self, board_with_both_main_ends):
        """Test that lateral branches unlock when both main ends filled."""
        assert board_with_both_main_ends.lateral_unlocked is True

    def test_cannot_add_lateral_before_unlock(self):
        """Test that lateral branches cannot be used before unlocking."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))

        with pytest.raises(ValueError) as exc_info:
            board.add_piece(DominoPiece(6, 3), EndType.LATERAL_TOP, connect_side=0)
        assert "Lateral branches only available" in str(exc_info.value)

    def test_can_add_lateral_top_after_unlock(self, board_with_both_main_ends):
        """Test adding piece to lateral top after unlock."""
        # Fill left end with value 2 to enable lateral (2)
        board_with_both_main_ends.add_piece(
            DominoPiece(2, 1), EndType.MAIN_LEFT, connect_side=1
        )

        # Now lateral with value 1
        position = board_with_both_main_ends.add_piece(
            DominoPiece(1, 4), EndType.LATERAL_TOP, connect_side=0
        )

        assert position.piece == DominoPiece(1, 4)
        assert board_with_both_main_ends.positions[EndType.LATERAL_TOP] is not None

    def test_can_add_lateral_bottom_after_unlock(self, board_with_both_main_ends):
        """Test adding piece to lateral bottom after unlock."""
        # Fill right end with value 4
        board_with_both_main_ends.add_piece(
            DominoPiece(4, 3), EndType.MAIN_RIGHT, connect_side=1
        )

        # Now lateral with value 3
        position = board_with_both_main_ends.add_piece(
            DominoPiece(3, 5), EndType.LATERAL_BOTTOM, connect_side=0
        )

        assert position.piece == DominoPiece(3, 5)
        assert board_with_both_main_ends.positions[EndType.LATERAL_BOTTOM] is not None


class TestEndValues:
    """Tests for getting end values."""

    def test_empty_board_returns_zero(self):
        """Test that empty board ends return 0."""
        board = DominoBoard()
        ends = board.get_current_ends()
        assert all(v == 0 for v in ends.values())

    def test_single_caroca_6_6(self):
        """Test end values with 6-6 caroca."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))

        ends = board.get_current_ends()
        assert ends[EndType.MAIN_LEFT] == 12  # Double sum
        assert ends[EndType.MAIN_RIGHT] == 12  # Double sum

    def test_after_adding_regular_piece(self):
        """Test end values after adding regular piece."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))
        board.add_piece(DominoPiece(6, 4), EndType.MAIN_RIGHT, connect_side=0)

        ends = board.get_current_ends()
        assert ends[EndType.MAIN_LEFT] == 12  # Caroca sum
        assert ends[EndType.MAIN_RIGHT] == 4  # Free side of new piece

    def test_filled_ends_count(self):
        """Test filled ends count is correct."""
        board = DominoBoard()
        assert board.get_filled_ends_count() == 0

        board.add_starting_piece(DominoPiece(6, 6))
        assert board.get_filled_ends_count() == 2  # Both main ends set

        board.add_piece(DominoPiece(6, 4), EndType.MAIN_LEFT, connect_side=0)
        assert board.get_filled_ends_count() == 3


class TestValidMoves:
    """Tests for validating and finding valid moves."""

    @pytest.fixture
    def board_with_multiple_pieces(self):
        """Fixture with multiple pieces on board."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))
        board.add_piece(DominoPiece(6, 4), EndType.MAIN_RIGHT, connect_side=0)
        board.add_piece(DominoPiece(6, 2), EndType.MAIN_LEFT, connect_side=1)
        return board

    def test_is_valid_move_positive(self, board_with_multiple_pieces):
        """Test is_valid_move returns True for valid move."""
        assert board_with_multiple_pieces.is_valid_move(
            DominoPiece(4, 1), EndType.MAIN_RIGHT
        ) is True

    def test_is_valid_move_negative(self, board_with_multiple_pieces):
        """Test is_valid_move returns False for invalid move."""
        assert board_with_multiple_pieces.is_valid_move(
            DominoPiece(1, 2), EndType.MAIN_RIGHT  # Doesn't have 4
        ) is False

    def test_get_valid_moves(self, board_with_multiple_pieces):
        """Test getting all valid moves for a piece."""
        valid_moves = board_with_multiple_pieces.get_valid_moves(
            DominoPiece(4, 3)
        )

        # Should be able to connect 4 to MAIN_RIGHT (value 4)
        assert EndType.MAIN_RIGHT in valid_moves
        # Should NOT be able to connect to MAIN_LEFT (value 2)
        assert EndType.MAIN_LEFT not in valid_moves

    def test_get_valid_moves_multiple_ends(self, board_with_multiple_pieces):
        """Test piece can match multiple ends."""
        valid_moves = board_with_multiple_pieces.get_valid_moves(
            DominoPiece(4, 6)
        )

        # Can match 4 on right and 6 on left (if available)
        # At least MAIN_RIGHT should be valid
        assert len(valid_moves) >= 1


class TestBoardStringRepresentation:
    """Tests for board string representation."""

    def test_str_format(self):
        """Test board string contains useful info."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))

        board_str = str(board)
        assert "DominoBoard" in board_str
        assert "lateral_unlocked" in board_str
