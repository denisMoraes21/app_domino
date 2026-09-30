# Domino Amazonense Implementation Research Findings

## Executive Summary

This document contains implementation research findings for the Domino Amazonense application with progressive 4-ends scoring system.

---

## Research Topic 1: GUI Framework Selection

### Decision: PyQt6 with QSS Styling

### Rationale

For a domino game requiring "mesa de bar" (bar table) aesthetic with dark wood, green felt, and amber tones, **PyQt6** provides the best balance of:

| Criteria | PyQt6 | tkinter | Kivy | PyWebview |
|----------|-------|---------|------|-----------|
| Custom Styling | Excellent (QSS) | Limited | Good (Kivy Language) | Excellent (CSS) |
| Graphics Performance | Excellent | Poor | Good | Excellent |
| Cross-Platform | Excellent | Excellent | Good | Good |
| Learning Curve | Medium | Low | Medium-High | Medium |
| Native Look | Yes | Yes | No | Browser-based |
| "Bar Table" Suitability | **Best** | Fair | Good | Very Good |

### Why PyQt6 Wins

1. **QSS (Qt Style Sheets)**: CSS-like syntax for realistic wood/felt textures
2. **Custom Widgets**: Easy subclassing for domino piece rendering with QPainter
3. **Graphics View Framework**: High-performance rendering for board animation
4. **Professional Look**: Polished UI across Windows, macOS, Linux
5. **Large Ecosystem**: Extensive documentation and community support

### Implementation Example - Mesa de Bar Widget

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class BarTableWidget(QWidget):
    """Base widget with bar table aesthetic"""
    
    def apply_bar_style(self):
        """Apply mesa de bar color scheme"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2d1810,
                    stop: 0.5 #1a3a1a,
                    stop: 1 #2d1810
                );
                border: 2px solid #4a3010;
                border-radius: 8px;
            }
        """)
```

### Color Palette for Mesa de Bar

| Element | Hex Code | Description |
|---------|----------|-------------|
| Wood border | `#4a3010` | Dark walnut |
| Felt surface | `#1a3a1a` | Deep forest green |
| Felt highlight | `#2d5a2d` | Lighter green |
| Amber accent | `#f0d9b5` | Ivory/cream |
| Wood highlight | `#f5e6d3` | Light amber |
| Text | `#f0d9b5` | Ivory text on dark |

---

## Research Topic 2: Progressive 4-Ends Board Data Structure

### Decision: Graph-Based Board with EndType Tracking

### Rationale

The progressive 4-ends system requires:
- Central starting piece (caroca)
- Two main ends that expand independently
- Conditional lateral branches (only after both main ends filled)
- Tracking filled/unfilled ends for scoring

A **directed graph with EndType markers** provides the flexibility needed.

### Data Model Implementation

**File: `src/domino/domain/board.py`**

```python
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict, Literal

class EndType(Enum):
    """Types of ends on the domino board"""
    MAIN_LEFT = auto()      # Primary left end
    MAIN_RIGHT = auto()     # Primary right end  
    LATERAL_TOP = auto()    # Branch top (unlocked after 2 main ends)
    LATERAL_BOTTOM = auto() # Branch bottom (unlocked after 2 main ends)

@dataclass(frozen=True)
class BoardPosition:
    """A position on the board containing a piece"""
    piece: DominoPiece
    orientation: Literal['longitudinal', 'transversal'] = 'longitudinal'
    connected_to: Optional[EndType] = None

    @property
    def free_side_value(self) -> int:
        """Value at the free (outer) end"""
        if self.orientation == 'transversal':
            return self.piece.get_total_value()  # Double sum
        return self.piece.side_b

@dataclass
class DominoBoard:
    """Graph-based board for progressive 4-ends system"""
    
    positions: Dict[EndType, Optional[BoardPosition]] = field(
        default_factory=lambda: {
            EndType.MAIN_LEFT: None,
            EndType.MAIN_RIGHT: None,
            EndType.LATERAL_TOP: None,
            EndType.LATERAL_BOTTOM: None,
        }
    )
    
    caroca: Optional[BoardPosition] = None
    lateral_unlocked: bool = False
    game_started: bool = False

    def get_current_ends(self) -> Dict[EndType, int]:
        """Get values at each end (0 for unfilled)"""
        result = {}
        for end_type, position in self.positions.items():
            if position is None:
                result[end_type] = 0  # Unfilled = 0 for scoring
            else:
                result[end_type] = position.free_side_value
        return result

    def _check_lateral_unlock(self) -> None:
        """Unlock lateral branches when both main ends are filled"""
        left_filled = self.positions[EndType.MAIN_LEFT] is not None
        right_filled = self.positions[EndType.MAIN_RIGHT] is not None
        self.lateral_unlocked = left_filled and right_filled
```

### Board Progression States

```
State 1: Initial (Caroca Only)
        [6|6]  <- Both main left and right point to this
    Filled: 2 ends

State 2: Main Ends Expanding
    [4]—[6|6]—[2]
    Filled: 2 ends

State 3: Lateral Unlocked
          [3]
          |
    [4]—[6|6]—[2]
    Filled: 3 ends, lateral_unlocked=True

State 4: Four Pontas (Full Board)
          [3]
          |
    [1]—[6|6]—[2]
          |
          [5]
    Filled: 4 ends
```

---

## Research Topic 3: Progressive Scoring Logic

### Decision: Type-Safe Service Pattern with Domain Events

### Rationale

Scoring logic is complex and requires:
- Clear type hints for maintainability
- Testability for TDD
- Separation from UI and game flow
- Event-driven architecture for Clean Architecture compliance

### Implementation Pattern

**File: `src/domino/domain/scorer.py`**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ScoredEvent:
    """Domain event for scoring actions"""
    player_id: str
    points: int
    ends_sum: int
    multiplier: int
    stage: str
    phase: str

class ProgressiveScorer:
    """Handles progressive 4-ends scoring for Domino Amazonense"""
    
    POINTS_DIVISOR = 5
    MULTIPLIER_MAP = {1: 1, 2: 2, 4: 4}
    
    def calculate(self, board: DominoBoard, player_id: str) -> Optional[ScoredEvent]:
        """Calculate score if ends sum to multiple of 5"""
        ends_values = board.get_current_ends()
        filled_count = board.get_filled_ends_count()
        
        if filled_count == 0:
            return None
        
        total_sum = sum(ends_values.values())
        
        if total_sum % self.POINTS_DIVISOR != 0:
            return None
        
        base_points = total_sum // self.POINTS_DIVISOR
        multiplier = self._get_multiplier(filled_count)
        final_points = base_points * multiplier
        
        return ScoredEvent(
            player_id=player_id,
            points=final_points,
            ends_sum=total_sum,
            multiplier=multiplier,
            stage=self._get_stage_name(filled_count),
            phase=self._get_phase(board).value
        )
    
    def _get_multiplier(self, filled_count: int) -> int:
        return self.MULTIPLIER_MAP.get(filled_count, 1)
    
    def _get_stage_name(self, filled_count: int) -> str:
        stages = {
            1: "Caroca \u00fanica",
            2: "Caroca + Ponta",
            4: "4 Pontas",
        }
        return stages.get(filled_count, f"{filled_count} pontas")
```

### Batida and Bloqueio Scoring

```python
@dataclass
class BatidaResult:
    """Result of batida (empty hand) game end"""
    winner_id: str
    points_awarded: int

class BatidaCalculator:
    """Calculate batida scores"""
    
    def calculate(self, winner_id: str, players: dict) -> BatidaResult:
        """Winner gets sum of all opponents' hand points"""
        total = sum(
            self._count_points(hands)
            for pid, hands in players.items()
            if pid != winner_id
        )
        return BatidaResult(winner_id=winner_id, points_awarded=total)

class BloqueioCalculator:
    """Calculate bloqueio (blocked game) scores"""
    
    def determine_winner(self, players: dict) -> str:
        """Player with fewest points in hand wins"""
        hand_scores = {
            pid: self._count_points(hands)
            for pid, hands in players.items()
        }
        return min(hand_scores, key=hand_scores.get)
```

---

## Project Structure

```
app_domino/
├── src/domino/
│   ├── __init__.py
│   ├── core.py                  # Clean Architecture layers
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── piece.py             # DominoPiece entity
│   │   ├── board.py             # DominoBoard aggregate
│   │   ├── scorer.py            # ProgressiveScorer service
│   │   └── events.py            # Domain events
│   ├── application/
│   │   └── ...                  # Use cases (future)
│   ├── infrastructure/
│   │   └── ...                  # Repositories (future)
│   └── gui/
│       └── main.py              # PyQt6 GUI with mesa de bar style
├── tests/
│   ├── domain/
│   │   ├── test_piece.py
│   │   ├── test_board.py
│   │   └── test_scorer.py
│   └── application/
├── pyproject.toml
├── requirements.txt
└── IMPLEMENTATION_FINDINGS.md
```

---

## Key Design Decisions

| Component | Decision | Alternative Considered |
|-----------|----------|----------------------|
| GUI Framework | PyQt6 with QSS | Tkinter (limited styling), Kivy (learning curve), PyWebview (complexity) |
| Board Model | Graph with EndType enum | Tree structure (harder lateral navigation), Adjacency list (overkill) |
| Scoring Pattern | Service class with events | Simple function (less extensible), Singleton (harder to test) |
| Type System | Full type hints with dataclasses | TypedDict (less structured), Protocol (more complex) |
| Architecture | Clean Architecture (domain-first) | MVC (mixed concerns), Monolithic (harder to test) |

---

## Next Steps for Implementation

1. ✅ **Complete** - Domain models (Piece, Board, Scorer)
2. ✅ **Complete** - Domain events and event dispatcher
3. ✅ **Complete** - TDD test suites (80%+ coverage target)
4. ✅ **Complete** - PyQt6 GUI prototype with mesa de bar styling
5. ⏳ **TODO** - Application layer (use cases, game controller)
6. ⏳ **TODO** - Infrastructure layer (persistence, configuration)
7. ⏳ **TODO** - Integration tests
8. ⏳ **TODO** - GUI polish and animations
9. ⏳ **TODO** - Multiplayer/network support (if needed)

---

## Scoring Rules Reference

| Situation | Condition | Multiplier | Formula |
|-----------|-----------|------------|---------|
| Caroca \u00fanica | 1 end filled | 1x | sum / 5 × 1 |
| Caroca + Ponta | 2 ends filled | 2x | sum / 5 × 2 |
| 4 Pontas | 4 ends filled | 4x | sum / 5 × 4 |
| Pass | No points | - | No penalty |
| Batida | Empty hand | - | Opponent hand sum |
| Bloqueio | No moves | - | Lowest hand wins |

**Important**: Only score when sum is multiple of 5. Unfilled ends = 0.
