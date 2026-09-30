# Pesquisa Técnica: Domino Amazonense

**Criado**: 2026-09-30

**Baseado em**: IMPLEMENTATION_FINDINGS.md e especificação funcional

---

## Resumo de Decisões

| Decisão | Escolha | Razão |
|---------|---------|-------|
| Linguagem | Python 3.12 | Especificado pelo usuário |
| Testes | pytest | Padrão indústria, fixtures poderosas |
| Validação | Pydantic v2 | Type hints integrados, validação automática |
| Linting | ruff + mypy | Rápido e estrito |
| Interface inicial | Web para computador | Navegador; frontend a definir, motor Python |

---

## Decisão 1: Estrutura de Dados para Mesa com 4 Pontas

**Regra confirmada**: As duas pontas laterais saem da carroça inicial. Só ficam disponíveis após jogar pelo menos uma pedra em cada uma das duas pontas principais; a carroça inicial não conta como preenchimento desses ramos. Jogar várias pedras apenas em uma ponta principal não libera as laterais. A primeira pedra de cada lateral deve combinar com o naipe da carroça inicial.

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

**Exceção — carroça final**: Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez.

**Pontuação confirmada**: Na tranca e na batida normal (sem carroça final), a dupla vencedora recebe a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo: `pontos = (soma_adversária // 5) * 5`. Somar as duas mãos antes de arredondar; não incluir a mão do parceiro nem subtrair a soma da dupla vencedora.

```python
# Passe geral é evento durante a raia, não condição de término.
# Registrar autor da última jogada e passes dos outros três jogadores.
# Confirmar que o último autor tem jogada antes de conceder passe geral.
# Se os quatro passam, é jogo fechado (tranca), sem bônus de galo.
# Passe comum: 20; segundo consecutivo: 0; passe geral: total de 50.
# Ao confirmar passe geral, substituir os pontos de passe da sequência,
# devolver a vez ao autor da última jogada e manter a raia em andamento.
# Reiniciar sequência após jogada válida; não pontuar o mesmo evento duas vezes.

class BatidaDetector:
    @staticmethod
    def has_batida(player: Player) -> bool:
        """Verifica se jogador esvaziou a mão."""
        return len(player.hand) == 0

class TrancaResolver:
    @staticmethod
    def resolve_tranca(pair_totals: dict[int, int]) -> tuple[int | None, dict[int, int]]:
        """Recebe as somas brutas das mãos das duas duplas."""
        if len(pair_totals) != 2:
            raise ValueError("Tranca exige exatamente duas duplas")
        points = {pair_id: 0 for pair_id in pair_totals}
        if len(set(pair_totals.values())) == 1:
            return None, points
        winner = min(pair_totals, key=lambda pair_id: pair_totals[pair_id])
        loser = next(pair_id for pair_id in pair_totals if pair_id != winner)
        points[winner] = (pair_totals[loser] // 5) * 5
        return winner, points
```

**Razão**:
- Cada condição isolada e testável
- Estado de passes tracking simples
- Empate na tranca não concede pontos a nenhuma dupla

---

## Decisão 5: Interface Gráfica Inicial

A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega. A mesa e as pedras terão estilo mesa de bar. O fluxo de jogo será operado por controles visuais; uma CLI de jogo não faz parte da entrega inicial. A interface web e sua integração com o motor ainda precisam ser implementadas.

Implementar interface web ligada ao motor Python. Preservar o protótipo PyQt6 como referência histórica, sem torná-lo dependência do cliente web. Os controles visuais invocam casos de uso e recebem o estado atualizado; a interface não decide pontuação ou validade das jogadas. Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista. Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

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
| Interface inicial | Web para computador | Plataforma definida; frontend a definir |
| Testes | pytest, 100+ testes, 80% coverage | ✅ Definido |

**Próximo passo**: Implementar Iteração 1 (entidades de domínio) seguindo o TDD.
