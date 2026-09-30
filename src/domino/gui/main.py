"""GUI module for Domino Amazonense - Mesa de Bar aesthetic."""

import sys
from pathlib import Path

# Add src to path for development
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtGui import (
    QFont, QColor, QPainter, QPixmap, QPainterPath,
    QPalette, QLinearGradient, QIcon
)
from PyQt6.QtCore import Qt, QRectF, QPointF

# Import domain models
from domino.domain.piece import DominoPiece
from domino.domain.board import DominoBoard, EndType


class DominoPieceWidget(QFrame):
    """
    Custom widget to render a domino piece with mesa de bar styling.

    Features:
    - Dark wood border
    - Ivory/cream colored tile
    - Black dots for pips
    - Rounded corners
    """

    def __init__(self, piece: DominoPiece, parent=None):
        super().__init__(parent)
        self.piece = piece
        self.setFixedSize(120, 60)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        """Custom painting for domino piece."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Outer wood border
        border_path = QPainterPath()
        border_path.addRoundedRect(0, 0, 120, 60, 8, 8)
        painter.fillPath(border_path, QColor(0x4a3010))

        # Ivory tile body
        tile_rect = QRectF(4, 4, 112, 52)
        tile_path = QPainterPath()
        tile_path.addRoundedRect(tile_rect, 6, 6)

        # Ivory gradient
        gradient = QLinearGradient(0, 0, 0, 52)
        gradient.setColorAt(0, QColor(0xf5e6d3))
        gradient.setColorAt(0.5, QColor(0xf0d9b5))
        gradient.setColorAt(1, QColor(0xe8c39e))
        painter.fillPath(tile_path, gradient)

        # Divider line
        painter.setPen(QColor(0x3d2810))
        painter.drawLine(60, 6, 60, 54)

        # Draw pips (dots)
        painter.setBrush(QColor(0x1a1a1a))
        painter.setPen(Qt.PenStyle.NoPen)

        # Calculate pip positions for both sides
        self._draw_pips(painter, self.piece.side_a, top=True)
        self._draw_pips(painter, self.piece.side_b, top=False)

    def _draw_pips(self, painter: QPainter, value: int, top: bool):
        """Draw pips for a given value on specified side."""
        center_x = 30 if top else 90
        center_y = 30

        # Pip positions for each value
        pip_positions = {
            0: [],
            1: [(center_x, center_y)],
            2: [(20, 20), (40, 40)],
            3: [(20, 20), (center_x, center_y), (40, 40)],
            4: [(20, 20), (40, 20), (20, 40), (40, 40)],
            5: [(20, 20), (40, 20), (center_x, center_y), (20, 40), (40, 40)],
            6: [(20, 20), (40, 20), (20, 30), (40, 30), (20, 40), (40, 40)],
        }

        for x, y in pip_positions.get(value, []):
            offset_y = -15 if top else 15
            painter.drawEllipse(QPointF(x, center_y + offset_y), 5, 5)


class BoardDisplayWidget(QWidget):
    """
    Widget to display the domino board with progressive 4-ends layout.

    Layout:
           [Top]
             |
    [Left] - [Caroca] - [Right]
             |
          [Bottom]
    """

    def __init__(self, board: DominoBoard, parent=None):
        super().__init__(parent)
        self.board = board
        self.setMinimumSize(400, 400)

    def paintEvent(self, event):
        """Custom painting for board display."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw felt background
        self._draw_felt_background(painter)

        # Draw board connection lines
        self._draw_board_lines(painter)

        # Draw caroca
        if self.board.caroca:
            self._draw_caroca(painter)

    def _draw_felt_background(self, painter: QPainter):
        """Draw green felt texture background."""
        rect = self.rect()

        # Felt gradient (darker edges)
        gradient = QLinearGradient(
            rect.center().x(), rect.top(),
            rect.center().x(), rect.bottom()
        )
        gradient.setColorAt(0, QColor(0x1a3a1a))
        gradient.setColorAt(0.3, QColor(0x2d5a2d))
        gradient.setColorAt(0.7, QColor(0x2d5a2d))
        gradient.setColorAt(1, QColor(0x1a3a1a))

        painter.fillRect(rect, gradient)

        # Optional: Add subtle felt texture
        painter.setPen(QColor(0x1e401e))
        for y in range(0, rect.height(), 10):
            painter.drawLine(0, y, rect.width(), y)

    def _draw_board_lines(self, painter: QPainter):
        """Draw connecting lines between board positions."""
        painter.setPen(QColor(0x3d2810))

        center = self.rect().center()
        cx, cy = center.x(), center.y()

        # Draw lines to corners
        painter.drawLine(cx - 100, cy, cx - 150, cy)  # Left
        painter.drawLine(cx + 100, cy, cx + 150, cy)  # Right
        painter.drawLine(cx, cy - 100, cx, cy - 150)  # Top
        painter.drawLine(cx, cy + 100, cx, cy + 150)  # Bottom

    def _draw_caroca(self, painter: QPainter):
        """Draw the central caroca piece."""
        center = self.rect().center()
        piece_widget = DominoPieceWidget(self.board.caroca.piece)
        piece_widget.move(center.x() - 60, center.y() - 30)


class GameWindow(QMainWindow):
    """Main game window with mesa de bar aesthetic."""

    def __init__(self):
        super().__init__()
        self.board = DominoBoard()
        self.setup_ui()
        self.apply_bar_style()

    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Domino Amazonense - Mesa de Bar")
        self.setMinimumSize(800, 600)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Header
        header = QLabel("DOMINO AMAZONSENSE")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #f0d9b5;
                padding: 10px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2d1810,
                    stop: 1 #1a0a00
                );
                border-bottom: 2px solid #4a3010;
            }
        """)
        layout.addWidget(header)

        # Board area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #4a3010;
                border-radius: 8px;
                background: qradialgradient(
                    cx: 0.5, cy: 0.5, radius: 1.0,
                    fx: 0.5, fy: 0.5,
                    stop: 0 #2d5a2d,
                    stop: 1 #1a3a1a
                );
            }
        """)

        board_display = BoardDisplayWidget(self.board)
        scroll.setWidget(board_display)
        layout.addWidget(scroll)

        # Controls area
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)

        info_label = QLabel("Jogo iniciado. Coloque a primeira pedra (caroca).")
        info_label.setStyleSheet("color: #f0d9b5; font-size: 14px;")
        controls_layout.addWidget(info_label)

        layout.addWidget(controls)

        # Status bar
        self.statusBar().showMessage("Bem-vindo ao Domino Amazonense")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: #2d1810;
                color: #f0d9b5;
                border-top: 1px solid #4a3010;
            }
        """)

    def apply_bar_style(self):
        """Apply the mesa de bar color scheme to the window."""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2d1810,
                    stop: 0.3 #1a281a,
                    stop: 0.7 #1a281a,
                    stop: 1 #2d1810
                );
            }
        """)


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = GameWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
