# Modelo de Dados: Domino Amazonense

**Criado**: 2026-09-30

**Baseado em**: Especificação funcional e pesquisa técnica

---

## Visão Geral do Domínio

```
┌─────────────────────────────────────────────────────────────┐
│                      PARTIDA (Match)                         │
│  - 2 Duplas (Pair)                                          │
│  - Pontuação acumulada                                      │
│  - Estado: INIT → INICIADA → EM_ANDAMENTO → FINALIZADA     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ contém
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        RAIA (Round)                          │
│  - Mesa (Board) com 4 pontas                                │
│  - Histórico de jogadas                                     │
│  - Estado: INIT → BATIDA → GALO → TRANCA                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ contém
                              ▼
┌─────────────────────┐         ┌─────────────────────┐
│   JOGADOR (Player)  │◄────────│    PEDRA (Piece)    │
│  - Mão de 7 pedras  │         │  - lado_a: 0-6      │
│  - Participa de 1   │         │  - lado_b: 0-6      │
│    Dupla            │         │  - is_doble: bool   │
└─────────────────────┘         └─────────────────────┘
      │                                    ▲
      │ pertence                           │ jogada em
      ▼                                    │
┌─────────────────────┐                    │
│    DUPLA (Pair)     │────────────────────┘
│  - 2 Jogadores      │  mesa contém
│  - Pontuação total  │
└─────────────────────┘
```

---

## Entidades de Domínio

### 1. Piece (Pedra)

**Responsabilidade**: Representar uma peça do dominó (duplo-6)

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| side_a | int | Valor do primeiro lado (0-6) |
| side_b | int | Valor do segundo lado (0-6) |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `is_doble() -> bool` | bool | True se side_a == side_b |
| `matches(value: int) -> bool` | bool | True se algum lado == value |
| `get_matching_side(value: int) -> int` | int | Lado que combina com value |
| `flip() -> Piece` | Piece | Retorna peça com lados invertidos |
| `total() -> int` | int | Soma dos dois lados |

**Regras de Validação**:
- side_a e side_b devem estar entre 0 e 6 (inclusivo)
- Piece é imutável após criação

**Exemplos**:
```python
piece = Piece(3, 5)
piece.is_doble()           # False
piece.matches(3)           # True
piece.matches(5)           # True
piece.matches(4)           # False
piece.get_matching_side(3) # 3
piece.flip()               # Piece(5, 3)
piece.total()              # 8

caroca = Piece(6, 6)
caroca.is_doble()          # True
```

---

### 2. Player (Jogador)

**Responsabilidade**: Representar um jogador com sua mão de pedras

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| id | int | Identificador único (0-3) |
| name | str | Nome do jogador |
| pair_id | int | ID da dupla que pertence (0 ou 1) |
| hand | list[Piece] | Pedras na mão (máx 7) |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `has_playable_piece(board: Board) -> bool` | bool | Tem pedra que combina com alguma ponta? |
| `get_playable_pieces(board: Board) -> list[Piece]` | list[Piece] | Lista de jogáveis |
| `play(piece: Piece, target_end: EndType) -> None` | None | Joga pedra na mesa |
| `pass_turn() -> None` | None | Marca jogador como passado |
| `get_hand_value() -> int` | int | Soma dos valores das pedras |
| `add_piece(piece: Piece) -> None` | None | Adiciona pedra à mão |

**Regras**:
- hand inicial sempre 7 pedras
- Não pode jogar peça que não combina com pontas
- pass_turn() só permitido se não tiver jogável

**Exemplos**:
```python
player = Player(id=0, name="Denis", pair_id=0)
player.add_piece(Piece(3, 5))
player.add_piece(Piece(6, 6))
player.get_hand_value()    # 3 + 5 + 6 + 6 = 20
player.has_playable_piece(board)  # False se nenhuma combinação
```

---

### 3. Pair (Dupla)

**Responsabilidade**: Agrupar 2 jogadores e gerenciar pontuação coletiva

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| id | int | ID da dupla (0 ou 1) |
| players | list[Player] | Os 2 jogadores da dupla |
| total_score | int | Pontuação acumulada na partida |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `add_points(points: int) -> None` | None | Adiciona pontos à pontuação total |
| `get_total_hand_points() -> int` | int | Soma das pedras de ambos jogadores |
| `get_active_player() -> Player` | Player | Retorna jogador da vez (alternar) |
| `has_playable_piece(board: Board) -> bool` | bool | Algum jogador da dupla tem jogável? |

**Regras**:
- Sempre exatamente 2 jogadores
- Pontuação é compartilhada
- Em batida, conta-se pedras da dupla adversária

---

### 4. EndType (Tipo de Ponta)

**Responsabilidade**: Enumerar os 4 tipos de pontas da mesa

**Valores**:
| Valor | Descrição |
|-------|-----------|
| MAIN_LEFT | Ponta principal esquerda |
| MAIN_RIGHT | Ponta principal direita |
| LATERAL_TOP | Rama lateral superior |
| LATERAL_BOTTOM | Rama lateral inferior |

**Regras**:
- LATERAL_TOP e LATERAL_BOTTOM só disponíveis após MAIN_LEFT e MAIN_RIGHT preenchidas

---

### 5. Board (Mesa)

**Responsabilidade**: Representar o estado da mesa com 4 pontas progressivas

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| _ends | dict[EndType, Optional[int]] | Valor de cada ponta (None = vazia) |
| _pieces_played | list[Piece] | Histórico de pedras jogadas |
| _first_piece | Optional[Piece] | Primeira pedra jogada (caroça inicial) |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `play_piece(piece: Piece, target_end: EndType) -> None` | None | Joga pedra na ponta alvo |
| `get_end_value(end_type: EndType) -> Optional[int]` | int or None | Valor da ponta específica |
| `get_available_ends() -> list[EndType]` | list[EndType] | Pontas disponíveis para jogar |
| `get_filled_ends() -> list[EndType]` | list[EndType] | Pontas já preenchidas |
| `get_all_end_values() -> list[int]` | list[int] | Valores [v1, v2, v3, v4] com 0 para vazias |
| `get_pieces_count() -> int` | int | Total de pedras na mesa |
| `is_empty() -> bool` | bool | Mesa sem pedras |
| `is_lateral_unlocked() -> bool` | bool | Laterais disponíveis? |

**Regras de Negócio**:
1. Mesa inicia vazia
2. Primeira pedra define MAIN_LEFT e MAIN_RIGHT (se doble) ou apenas 1 ponta
3. Segunda pedra cria segunda ponta principal
4. Após ambas principais preenchidas, laterais são desbloqueadas
5. Máximo 4 pontas simultâneas

**Estados da Mesa**:
```
EMPTY → ONE_END → TWO_ENDS → FOUR_ENDS (com laterais desbloqueadas)
```

**Exemplos**:
```python
board = Board()
board.is_empty()  # True

board.play_piece(Piece(6, 6), EndType.MAIN_LEFT)  # Doble inicial
board.get_end_value(EndType.MAIN_LEFT)   # 12 (soma dos dois lados: 6+6)
board.get_available_ends()  # [MAIN_LEFT]

board.play_piece(Piece(6, 3), EndType.MAIN_LEFT)
board.get_end_value(EndType.MAIN_RIGHT)  # 3
board.get_available_ends()  # [MAIN_LEFT, MAIN_RIGHT]

board.play_piece(Piece(3, 2), EndType.MAIN_RIGHT)
board.is_lateral_unlocked()  # True
board.get_available_ends()   # [MAIN_LEFT, MAIN_RIGHT, LATERAL_TOP, LATERAL_BOTTOM]
```

---

### 6. Score (Pontuação)

**Responsabilidade**: Valor de pontuação com validação

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| value | int | Valor numérico da pontuação |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `__init__(value: int)` | None | Valida value >= 0 |
| `__add__(other: Score) -> Score` | Score | Soma de pontuações |
| `__eq__(other: Score) -> bool` | bool | Igualdade de pontuações |
| `is_multiple_of_5() -> bool` | bool | True se value % 5 == 0 |

**Regras**:
- Nunca negativo
- Pontuação só marca quando soma das pontas % 5 == 0

---

### 7. Round (Raia)

**Responsabilidade**: Gerenciar uma rodada individual da partida

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| board | Board | Mesa atual |
| current_player_id | int | ID do jogador da vez |
| players | list[Player] | Todos os 4 jogadores |
| play_history | list[PlayRecord] | Histórico de jogadas |
| consecutive_passes | int | Contador de passes seguidos |
| state | RoundState | Estado atual da raia |
| winner_pair_id | Optional[int] | ID da dupla vencedora (se encerrada) |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `start() -> None` | None | Inicia raia (distribui pedras) |
| `play_piece(piece: Piece) -> Score` | Score | Executa jogada e retorna pontuação |
| `pass_turn() -> int` | int | Executa passe, retorna pontos adversários (20) |
| `check_end_conditions() -> Optional[RoundEndReason]` | RoundEndReason or None | Verifica batida/galo/tranca |
| `calculate_round_score() -> dict` | dict | Calcula pontuação final da raia |
| `get_current_player() -> Player` | Player | Jogador da vez atual |
| `next_player() -> None` | None | Avança para próximo jogador |

**Estados (RoundState)**:
| Estado | Descrição |
|--------|-----------|
| INIT | Raia criada, pedras não distribuídas |
| DEALT | Pedras distribuídas, aguardando primeira jogada |
| IN_PROGRESS | Jogadas sendo feitas |
| BATIDA | Alguém esvaziou a mão |
| GALO | Todos os 4 jogadores passaram |
| TRANCA | Jogo bloqueado (sem jogadas possíveis) |

**Condições de Término**:
1. **BATIDA**: Jogador joga última pedra (hand vazia). Se for carroça, bônus de 20 pontos.
2. **GALO**: 4 passes consecutivos
3. **TRANCA**: Nenhum jogador tem jogada válida (não é galo)

---

### 8. Match (Partida)

**Responsabilidade**: Gerenciar toda a partida completa

**Atributos**:
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| pairs | list[Pair] | As 2 duplas |
| current_round | int | Número da raia atual (1-indexed) |
| state | MatchState | Estado da partida |
| rounds_played | list[Round] | Histórico de raias |
| first_batida_pair_id | Optional[int] | Quem bateu na primeira raia |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `start() -> None` | None | Inicia primeira raia |
| `start_next_round() -> Round` | Round | Inicia próxima raia |
| `check_match_victory() -> Optional[int]` | int or None | Retorna ID da dupla vencedora (se >= 200) |
| `is_finished() -> bool` | bool | True se alguma dupla >= 200 pontos |
| `get_winner() -> Optional[int]` | int or None | ID da dupla vencedora |
| `get_scoreboard() -> dict` | dict | Mapa {pair_id: score} |

**Estados (MatchState)**:
| Estado | Descrição |
|--------|-----------|
| INIT | Partida não iniciada |
| IN_PROGRESS | Raias sendo jogadas |
| FINISHED | Partida encerrada (vencedor definido) |

**Regras**:
- Vitória ao atingir >= 200 pontos ao final de uma raia
- Quem bateu inicia próxima raia
- Partida pode ter múltiplas raias

---

## Enums

### RoundState
```python
class RoundState(Enum):
    INIT = auto()
    DEALT = auto()
    IN_PROGRESS = auto()
    BATIDA = auto()
    GALO = auto()
    TRANCA = auto()
```

### MatchState
```python
class MatchState(Enum):
    INIT = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
```

### RoundEndReason
```python
class RoundEndReason(Enum):
    BATIDA = auto()
    GALO = auto()
    TRANCA = auto()
```

---

## Eventos de Domínio

### PiecePlayedEvent
```python
@dataclass
class PiecePlayedEvent:
    player_id: int
    piece: Piece
    target_end: EndType
    board_state: dict[EndType, int]
    scored: bool
    points_earned: int
```

### RoundEndedEvent
```python
@dataclass
class RoundEndedEvent:
    round_number: int
    end_reason: RoundEndReason
    winner_pair_id: int
    scores_awarded: dict[int, int]  # {pair_id: points}
```

### MatchEndedEvent
```python
@dataclass
class MatchEndedEvent:
    winning_pair_id: int
    final_scores: dict[int, int]
    rounds_played: int
```

---

## Validadores

### MoveValidator
```python
class MoveValidator:
    @staticmethod
    def can_play(piece: Piece, board: Board, target_end: EndType) -> tuple[bool, str]:
        """
        Valida jogada. Retorna (ok, mensagem_erro).
        
        Erros possíveis:
        - "Ponta não disponível"
        - "Peça não combina com a ponta"
        - "Laterais bloqueadas"
        - "Mesa vazia - use start()"
        """
```

### PlayRestrictionsValidator
```python
class PlayRestrictionsValidator:
    @staticmethod
    def can_create_lateral_branch(board: Board) -> bool:
        """Laterais só podem ser criadas após MAIN_LEFT e MAIN_RIGHT preenchidos."""
```

---

## Resumo de Relacionamentos

```
Match (1) ── contém ──► Round (0..n)
Round (1) ── contém ──► Board (1)
Round (1) ── contém ──► Player (4)
Player (n) ── pertence ──► Pair (2)
Piece ── jogada em ──► Board
Score ── calculado por ──► ProgressiveScorer
```

---

## Notas de Implementação

1. **Imutabilidade**: Piece e Score são imutáveis
2. **Valores 0-6**: Todas as validações de peça usam 0-6
3. **4 pontas**: Board sempre suporta até 4 pontas, mesmo que não preenchidas
4. **Pontuação**: 0 para pontas vazias na soma progressiva
5. **Duplas**: IDs fixos (0 ou 1), jogadores distribuídos alternadamente
