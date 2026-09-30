"""Tests for progressive scoring logic."""

import pytest
from src.domino.domain.piece import DominoPiece
from src.domino.domain.board import DominoBoard, EndType
from src.domino.domain.scorer import (
    ProgressiveScorer,
    HandCounter,
    BatidaCalculator,
    BloqueioCalculator,
)


class TestProgressiveScorerBasic:
    """Tests for basic scoring functionality."""

    @pytest.fixture
    def scorer(self):
        """Create a ProgressiveScorer instance."""
        return ProgressiveScorer()

    def test_empty_board_no_score(self, scorer):
        """Test that empty board returns no score."""
        board = DominoBoard()
        result = scorer.calculate(board, "player1")
        assert result is None

    def test_board_not_multiple_of_five(self, scorer):
        """Test that non-multiple of 5 returns no score."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(1, 2))  # Sum = 3

        result = scorer.calculate(board, "player1")
        assert result is None

    def test_single_end_multiple_of_five(self, scorer):
        """Test scoring with single end (caroca)."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(5, 5))  # Sum = 10

        result = scorer.calculate(board, "player1")

        assert result is not None
        assert result.player_id == "player1"
        assert result.ends_sum == 10
        assert result.multiplier == 1
        assert result.points == 2  # 10 / 5 * 1

    def test_multiple_of_five_no_multiplier_yet(self, scorer):
        """Test that score requires filled ends > 0."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(6, 6))  # Sum = 12 (not multiple)

        result = scorer.calculate(board, "player1")
        assert result is None  # 12 is not multiple of 5


class TestProgressiveScorerMultiplier:
    """Tests for progressive multipliers."""

    @pytest.fixture
    def scorer(self):
        return ProgressiveScorer()

    def test_one_end_multiplier_1(self, scorer):
        """Test 1 end filled = 1x multiplier."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(5, 5))

        result = scorer.calculate(board, "player1")

        assert result.multiplier == 1
        assert result.stage == "Caroca \u00fanica"

    def test_two_ends_multiplier_2(self, scorer):
        """Test 2 ends filled = 2x multiplier."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(5, 5))

        # Add piece to one end to have 2 filled ends
        board.add_piece(DominoPiece(5, 5), EndType.MAIN_RIGHT, connect_side=0)

        # Sum = 10 (caroca) + 10 (piece) = 20
        result = scorer.calculate(board, "player1")

        assert result.multiplier == 2
        assert result.stage == "Caroca + Ponta"
        assert result.points == 8  # 20 / 5 * 2 = 8

    def test_four_ends_multiplier_4(self, scorer):
        """Test 4 ends filled = 4x multiplier."""
        board = DominoBoard()

        # Create a board that will have all 4 ends filled with sum = 20
        board.add_starting_piece(DominoPiece(5, 5))  # 10

        # Fill main right with 5-5
        board.add_piece(DominoPiece(5, 5), EndType.MAIN_RIGHT, connect_side=0)  # 10
        # Now right end = 10, left end = 10

        # Unlock lateral by filling left
        board.add_piece(DominoPiece(5, 3), EndType.MAIN_LEFT, connect_side=0)  # 8
        # Now left end = 3, unlock lateral

        # Lateral top with 3-2
        board.add_piece(DominoPiece(3, 2), EndType.LATERAL_TOP, connect_side=0)  # 5
        # Now top end = 2

        # Lateral bottom with 2-0
        board.add_piece(DominoPiece(2, 0), EndType.LATERAL_BOTTOM, connect_side=0)  # 2
        # Now bottom end = 0

        ends = board.get_current_ends()
        total = sum(ends.values())  # 10 + 10 + 2 + 0 = 22 (not multiple of 5)

        # Let's try again with values that sum to 20
        board2 = DominoBoard()
        board2.add_starting_piece(DominoPiece(3, 2))  # 5 (transversal = 5)
        board2.add_piece(DominoPiece(3, 1), EndType.MAIN_LEFT, connect_side=0)  # 1
        board2.add_piece(DominoPiece(2, 0), EndType.MAIN_RIGHT, connect_side=0)  # 0
        board2.add_piece(DominoPiece(1, 2), EndType.LATERAL_TOP, connect_side=0)  # 2
        board2.add_piece(DominoPiece(0, 0), EndType.LATERAL_BOTTOM, connect_side=0)  # 0

        ends2 = board2.get_current_ends()
        total2 = sum(ends2.values())  # 5 + 1 + 0 + 2 + 0 = 8

        # Need to carefully construct for sum = 20
        board3 = DominoBoard()
        board3.add_starting_piece(DominoPiece(5, 0))  # free = 0
        # Ends: left=0, right=0
        board3.add_piece(DominoPiece(0, 0), EndType.MAIN_LEFT, connect_side=0)  # free = 0
        board3.add_piece(DominoPiece(0, 0), EndType.MAIN_RIGHT, connect_side=0)  # free = 0
        # Now left filled, right filled, unlock lateral
        board3.add_piece(DominoPiece(0, 0), EndType.LATERAL_TOP, connect_side=0)  # free = 0
        board3.add_piece(DominoPiece(0, 0), EndType.LATERAL_BOTTOM, connect_side=0)  # free = 0

        ends3 = board3.get_current_ends()
        # All 4 ends are 0, sum = 0 (technically multiple of 5, but 0 points)

        result = scorer.calculate(board3, "player1")
        assert result.multiplier == 4
        assert result.points == 0  # 0 / 5 * 4 = 0


class TestHandCounter:
    """Tests for hand point counting."""

    @pytest.fixture
    def counter(self):
        return HandCounter()

    def test_count_pieces(self, counter):
        """Test counting pieces in hand."""
        pieces = [
            DominoPiece(1, 2),
            DominoPiece(3, 4),
            DominoPiece(5, 6),
        ]
        assert counter.count_pieces(pieces) == 3

    def test_count_points_simple(self, counter):
        """Test counting points in hand."""
        pieces = [
            DominoPiece(1, 2),  # 3
            DominoPiece(3, 4),  # 7
            DominoPiece(0, 0),  # 0
        ]
        assert counter.count_points(pieces) == 10

    def test_count_double_points(self, counter):
        """Test counting only double pieces' points."""
        pieces = [
            DominoPiece(1, 2),  # not double
            DominoPiece(3, 3),  # double = 6
            DominoPiece(5, 6),  # not double
            DominoPiece(6, 6),  # double = 12
        ]
        assert counter.count_double_points(pieces) == 18

    def test_count_empty_hand(self, counter):
        """Test counting empty hand."""
        assert counter.count_pieces([]) == 0
        assert counter.count_points([]) == 0


class TestBatidaCalculator:
    """Tests for batida (empty hand) scoring."""

    @pytest.fixture
    def batida_calc(self):
        return BatidaCalculator()

    def test_batida_single_opponent(self, batida_calc):
        """Test batida with single opponent."""
        winner_id = "player1"
        players = {
            "player1": [],  # Winner has no pieces
            "player2": [
                DominoPiece(1, 2),  # 3
                DominoPiece(3, 3),  # 6
            ],
        }

        result = batida_calc.calculate(winner_id, players)

        assert result.winner_id == "player1"
        assert result.points_awarded == 9  # 3 + 6

    def test_batida_multiple_opponents(self, batida_calc):
        """Test batida with multiple opponents."""
        winner_id = "player1"
        players = {
            "player1": [],
            "player2": [DominoPiece(6, 6)],  # 12
            "player3": [DominoPiece(5, 5)],  # 10
            "player4": [DominoPiece(1, 1)],  # 2
        }

        result = batida_calc.calculate(winner_id, players)

        assert result.winner_id == "player1"
        assert result.points_awarded == 24  # 12 + 10 + 2

    def test_batida_opponent_has_doubles(self, batida_calc):
        """Test batida when opponent has doubles."""
        winner_id = "player1"
        players = {
            "player1": [],
            "player2": [
                DominoPiece(6, 6),  # 12
                DominoPiece(5, 5),  # 10
            ],
        }

        result = batida_calc.calculate(winner_id, players)
        assert result.points_awarded == 22


class TestBloqueioCalculator:
    """Tests for bloqueio (blocked game) scoring."""

    @pytest.fixture
    def bloqueio_calc(self):
        return BloqueioCalculator()

    def test_bloqueio_single_winner(self, bloqueio_calc):
        """Test bloqueio with clear winner."""
        players = {
            "player1": [DominoPiece(1, 1)],  # 2 points
            "player2": [DominoPiece(3, 4), DominoPiece(2, 2)],  # 11 points
        }

        result = bloqueio_calc.determine_winner(players)

        assert result.winner_id == "player1"
        assert result.scores["player1"] == 2
        assert result.scores["player2"] == 11

    def test_bloqueio_tie_breaker_last_mover(self, bloqueio_calc):
        """Test bloqueio tie-breaker with last mover."""
        players = {
            "player1": [DominoPiece(2, 2)],  # 4 points
            "player2": [DominoPiece(1, 3)],  # 4 points
        }

        result = bloqueio_calc.determine_winner(players, last_mover="player2")

        assert result.winner_id == "player1"  # player2 was last mover, loses tie

    def test_bloqueio_tie_no_last_mover(self, bloqueio_calc):
        """Test bloqueio tie without last mover info."""
        players = {
            "player1": [DominoPiece(2, 2)],  # 4 points
            "player2": [DominoPiece(1, 3)],  # 4 points
        }

        result = bloqueio_calc.determine_winner(players)

        # Should pick first candidate
        assert result.winner_id in ["player1", "player2"]
        assert result.scores["player1"] == 4
        assert result.scores["player2"] == 4

    def test_bloqueio_all_same_points(self, bloqueio_calc):
        """Test bloqueio where all players have same points."""
        players = {
            "player1": [DominoPiece(1, 2)],  # 3 points
            "player2": [DominoPiece(0, 3)],  # 3 points
        }

        result = bloqueio_calc.determine_winner(players)
        assert result.winner_id in ["player1", "player2"]


class TestScorerProgressionInfo:
    """Tests for scoring progression information."""

    @pytest.fixture
    def scorer(self):
        return ProgressiveScorer()

    def test_progression_info_empty_board(self, scorer):
        """Test progression info for empty board."""
        board = DominoBoard()
        info = scorer.get_progression_info(board)

        assert info["filled_count"] == 0
        assert info["can_score"] is False
        assert info["lateral_available"] is False

    def test_progression_info_with_pieces(self, scorer):
        """Test progression info with pieces on board."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(5, 5))

        info = scorer.get_progression_info(board)

        assert info["filled_count"] == 2
        assert info["total_sum"] == 20  # 10 + 10
        assert info["can_score"] is True
        assert info["potential_points"] == 4  # 20 / 5 * 1

    def test_progression_lateral_unlocked(self, scorer):
        """Test progression info after lateral unlock."""
        board = DominoBoard()
        board.add_starting_piece(DominoPiece(5, 5))
        board.add_piece(DominoPiece(5, 3), EndType.MAIN_LEFT, connect_side=0)

        info = scorer.get_progression_info(board)

        assert info["lateral_available"] is True
