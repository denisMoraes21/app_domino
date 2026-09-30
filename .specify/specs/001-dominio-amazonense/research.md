# Pesquisa Técnica: Domino Amazonense

**Criado**: 2026-09-30

**Baseado em**: IMPLEMENTATION_FINDINGS.md e especificação funcional

---

## Resumo de Decisões

| Decisão | Escolha | Razão |
|---------|---------|-------|
| Linguagem | Python 3.12 | Especificado pelo usuário |
| Testes | pytest | Padrão indústria, fixtures poderosas |
| CLI | argparse | Sem dependências, simples para MVP |
| Validação | Pydantic v2 | Type hints integrados, validação automática |
| Linting | ruff + mypy | Rápido e estrito |
| GUI (futuro) | PyQt6 | Melhor para estética "mesa de bar" |

---

## Decisão 1: Estrutura de Dados para Mesa com 4 Pontas

**Problema**: Como representar uma mesa que evolui de 1 ponta → 2 pontas → 4 pontas com ramos laterais condicionais?

**Decisão**: Usar `dict[EndType, int]` com enum para tipos de ponta

```python
from enum import Enum, auto
from typing import Optional, Dict

class EndType(Enum):
    MAIN_LEFT = auto()      # Ponta principal esquerda
    MAIN_RIGHT = auto()     # Ponta principal direita
    LATERAL_TOP = auto()    # Rama lateral superior
    LATERAL_BOTTOM = auto() # Rama lateral inferior

class DominoBoard:
    def __init__(self):
        self._ends: Dict[EndType, Optional[int]] = {
            EndType.MAIN_LEFT: None,
            EndType.MAIN_RIGHT: None,
            EndType.LATERAL_TOP: None,
            EndType.LATERAL_BOTTOM: None,
        }
        self._pieces_played: list = []
    
    def get_available_ends(self) -> list[EndType]:
        """Retorna pontas disponíveis para jogar."""
        available = []
        for end_type, value in self._ends.items():
            if value is not None:
                available.append(end_type)
        # Lógica de desbloqueio de laterais
        if self._ends[EndType.MAIN_LEFT] is not None and \
           self._ends[EndType.MAIN_RIGHT] is not None:
            if self._ends[EndType.LATERAL_TOP] is None:
                available.append(EndType.LATERAL_TOP)
            if self._ends[EndType.LATERAL_BOTTOM] is None:
                available.append(EndType.LATERAL_BOTTOM)
        return available
```

**Razão**: 
- Simple e explícito
- Facilita validação de ramos laterais
- Permite acesso O(1) para cada ponta
- Fácil serialização para CLI/GUI

**Alternativas consideradas**:
- **Lista simples**: Não suporta ramos laterais
- **Grafo completo**: Excesso de complexidade para 4 pontas
- **Nested dict**: Difícil de manter estado consistente

---

## Decisão 2: Algoritmo de Validação de Jogadas

**Problema**: Como validar se uma peça pode ser jogada em uma ponta específica?

**Decisão**: Método `matches()` na peça + verificação de ponta disponível

```python
class Piece:
    def __init__(self, side_a: int, side_b: int):
        if not (0 <= side_a <= 6 and 0 <= side_b <= 6):
            raise ValueError("Valores da peça devem estar entre 0 e 6")
        self._side_a = side_a
        self._side_b = side_b
    
    def matches(self, end_value: int) -> bool:
        """Verifica se a peça combina com o valor da ponta."""
        return self._side_a == end_value or self._side_b == end_value
    
    def get_matching_side(self, end_value: int) -> int:
        """Retorna qual lado da peça combina com a ponta."""
        if self._side_a == end_value:
            return self._side_a
        return self._side_b
```

```python
class MoveValidator:
    @staticmethod
    def can_play(piece: Piece, board: DominoBoard, target_end: EndType) -> bool:
        """Valida se peça pode ser jogada na ponta alvo."""
        end_value = board.get_end_value(target_end)
        if end_value is None:
            return False
        return piece.matches(end_value)
```

**Razão**:
- Separação clara de responsabilidades
- Fácil de testar isoladamente
- Mensagens de erro específicas

---

## Decisão 3: Sistema de Pontuação Progressiva

**Problema**: Como calcular pontuação baseada no progresso da mesa?

**Decisão**: Serviço `ProgressiveScorer` com lógica explícita por fase

```python
class ProgressiveScorer:
    @staticmethod
    def calculate_score(board: DominoBoard) -> int:
        """
        Calcula pontuação baseada no estado da mesa:
        - 1 peça (carroça única): soma dos dois lados da carroça (ex: 6-6 = 12)
        - 2 peças: carroça + ponta jogada
        - 3-4 peças: pontas opostas + laterais (0 se vazias)
        - 5+ peças: soma completa das 4 pontas
        """
        ends = board.get_all_end_values()  # Retorna [v1, v2, v3, v4] com zeros
        
        # Contar quantas pontas estão preenchidas
        filled_ends = sum(1 for v in ends if v > 0 or board.is_end_filled(end))
        
        if filled_ends == 1:
            # Carroça única = soma dos dois lados
            caroca = next(p for p in board._pieces_played if p.is_doble())
            return caroca.total()  # side_a + side_b
        elif filled_ends == 2:
            # Duas pontas (carroça + primeira jogada)
            return sum(v for v in ends if v > 0)
        else:
            # 4 pontas (com zeros para não preenchidas)
            return sum(ends)
    
    @staticmethod
    def should_score(total: int) -> bool:
        """Verifica se a soma deve marcar pontos (múltiplo de 5)."""
        return total % 5 == 0
```

**Razão**:
- Lógica centralizada e testável
- Fácil de debugar e extender
- Separação entre cálculo e decisão de pontuar

---

## Decisão 4: Detecção de Condições de Término

**Problema**: Como detectar batida, galo e tranca de forma confiável?

**Decisão**: Detectores dedicados com estado de passes consecutivos

```python
class GaloDetector:
    def __init__(self):
        self._consecutive_passes = 0
    
    def record_pass(self):
        self._consecutive_passes += 1
    
    def record_play(self):
        self._consecutive_passes = 0
    
    def is_galo(self) -> bool:
        """Galo ocorre quando todos os 4 jogadores passaram."""
        return self._consecutive_passes >= 4

class BatidaDetector:
    @staticmethod
    def has_batida(player: Player) -> bool:
        """Verifica se jogador esvaziou a mão."""
        return len(player.hand) == 0

class TrancaResolver:
    @staticmethod
    def resolve_tranca(players: list[Player]) -> Player:
        """
        Resolve tranca: ganha quem tem MENOS pontos na mão.
        Empate: perde quem jogou por último.
        """
        player_scores = [(p, sum(p.get_hand_value())) for p in players]
        min_score = min(score for _, score in player_scores)
        winners = [p for p, s in player_scores if s == min_score]
        
        if len(winners) == 1:
            return winners[0]
        else:
            # Empate: perdedor é quem jogou por último
            return TrancaResolver._get_last_player(winners)
```

**Razão**:
- Cada condição isolada e testável
- Estado de passes tracking simples
- Lógica de desempate explícita

---

## Decisão 5: Biblioteca CLI

**Problema**: Qual biblioteca usar para interface de linha de comando?

**Decisão**: argparse (padrão Python) para MVP

**Razão**:
- Zero dependências
- Suficiente para comandos simples (start, play, pass, status)
- Pode evoluir para `click` ou `typer` se necessário

```python
import argparse

def create_cli():
    parser = argparse.ArgumentParser(description='Domino Amazonense CLI')
    subparsers = parser.add_subparsers(dest='command')
    
    # start command
    subparsers.add_parser('start', help='Iniciar nova partida')
    
    # play command
    play_parser = subparsers.add_parser('play', help='Jogar pedra')
    play_parser.add_argument('piece', help='Peça no formato X-Y (ex: 3-5)')
    
    # pass command
    subparsers.add_parser('pass', help='Passar a vez')
    
    # status command
    subparsers.add_parser('status', help='Mostrar estado atual')
    
    # score command
    subparsers.add_parser('score', help='Mostrar pontuação')
    
    return parser
```

**Alternativas consideradas**:
- **click**: Mais elegante, mas requer dependência
- **typer**: Moderno com type hints, mas overkill para MVP
- **repl**: Boa para interatividade, mas complexo de implementar

---

## Decisões de Testes

### Estrutura de Testes

```
tests/
├── domain/
│   ├── entities/
│   │   ├── test_piece.py        # 10-15 testes
│   │   ├── test_player.py       # 8-10 testes
│   │   ├── test_pair.py         # 5-8 testes
│   │   └── test_board.py        # 15-20 testes
│   └── events/
│       └── test_game_events.py  # 5-8 testes
├── application/
│   ├── services/
│   │   ├── test_scorer.py       # 15-20 testes
│   │   └── test_validator.py    # 10-15 testes
│   └── use_cases/
│       └── test_*.py            # 20-30 testes
└── infrastructure/
    └── generators/
        └── test_*.py            # 10-15 testes
```

**Total estimado**: 100-150 testes

### Configuração pytest

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--verbose",
    "--cov=src/domino",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.coverage.run]
source = ["src/domino"]
omit = ["*/interface/*"]  # CLI pode ter cobertura menor inicialmente

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## Resumo

| Área | Decisão | Status |
|------|---------|--------|
| Estrutura Board | Dict com EndType enum | ✅ Definido |
| Validação Jogadas | matches() + target_end | ✅ Definido |
| Pontuação | ProgressiveScorer | ✅ Definido |
| Condições Término | Detectores dedicados | ✅ Definido |
| CLI | argparse | ✅ Definido |
| Testes | pytest, 100+ testes, 80% coverage | ✅ Definido |

**Próximo passo**: Implementar Iteração 1 (entidades de domínio) seguindo o TDD.
