# Modelo de Dados: Domino Amazonense

**Criado**: 2026-09-30

**Baseado em**: Especificação funcional e pesquisa técnica

---

## Identidade do Participante

O jogador entra escolhendo um apelido, sem cadastro, login ou senha. No multiplayer, pode criar uma sala ou informar o código de uma sala existente.

O apelido é o nome de exibição. Manter um identificador de sessão anônima independente, reconhecido pelo serviço, para preservar a posição e a mão na reconexão. Informar o mesmo apelido não é prova de identidade nem autoriza acesso à mão de outro participante.

## Sala Multiplayer

O multiplayer começa pela criação de uma sala. A sala reúne quatro jogadores humanos, cada um no navegador de seu computador, para uma partida em duas duplas. Ao criar a sala, o sistema gera e exibe um código. Os demais jogadores entram informando esse código na interface web. No multiplayer, os próprios jogadores escolhem suas duplas na sala antes do início da partida. Cada dupla deve ter exatamente dois jogadores; a partida só pode começar com as duas duplas completas. As duplas permanecem fixas durante a partida. Quando os quatro jogadores estiverem na sala e houver exatamente dois em cada dupla, o sistema embaralha e distribui automaticamente as 28 pedras, sete por jogador, sem comando do criador da sala. Aplicam-se as regras de cinco, seis e sete carroças antes da primeira jogada; na primeira raia, quem receber o 6-6 inicia jogando essa pedra.

A sala identifica a sessão multiplayer e os participantes, com capacidade de quatro jogadores. A partida mantém o estado do jogo e as regras; a sala organiza o encontro dos participantes. O código identifica a sala para entrada dos demais jogadores e deve distinguir salas ativas. A sala inicia a distribuição automaticamente ao completar quatro jogadores com duas duplas de dois. O humano reconectado retoma sua posição no próximo turno que lhe couber. Na desconexão durante a partida, um computador assume a mesma posição e mão. A sala deve guardar as escolhas de dupla e impedir mais de dois participantes na mesma dupla.

## Tempo e Substituição de Participante

Durante a partida, se um jogador humano perder a conexão, um jogador controlado pelo computador assume seu lugar, preservando mão, dupla e estado da partida. Cada jogada tem limite de 20 segundos. Ao esgotar os 20 segundos, o computador executa uma jogada válida pelo jogador naquele turno. Se não houver jogada válida, executa o passe conforme as regras do jogo. Para um humano ainda conectado, essa ação automática não transfere permanentemente o controle ao computador. Após reconectar, o humano retoma sua mesma posição no início do próximo turno que lhe couber, preservando mão, dupla e estado atual. A reconexão não desfaz jogadas já realizadas pelo computador nem interrompe o turno em andamento.

Registrar separadamente a identidade do jogador e quem controla sua posição (humano ou computador). Manter um prazo de turno de 20 segundos controlado pelo serviço da partida e compartilhado com a interface. A substituição não cria outra mão nem outra dupla.

## Participação e Visões da Partida

A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega.

Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.

Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

Adicionar tipo de participante (humano ou computador) ao jogador e identificação da sessão no multiplayer. A forma de participação não muda as regras de pontuação. A visão enviada a cada dispositivo deve conter sua mão e o estado público, sem serializar as mãos alheias.

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
│  - Estado: INIT → IN_PROGRESS → BATIDA/TRANCA                   │
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
- Na tranca e na batida normal (sem carroça final), a dupla vencedora recebe a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo: `pontos = (soma_adversária // 5) * 5`. Somar as duas mãos antes de arredondar; não incluir a mão do parceiro nem subtrair a soma da dupla vencedora.

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
- As duas pontas laterais saem da carroça inicial. Só ficam disponíveis após jogar pelo menos uma pedra em cada uma das duas pontas principais; a carroça inicial não conta como preenchimento desses ramos. Jogar várias pedras apenas em uma ponta principal não libera as laterais. A primeira pedra de cada lateral deve combinar com o naipe da carroça inicial.

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
2. A carroça inicial oferece duas pontas principais para encaixe, ainda sem pedras adicionais em seus ramos
3. Registrar separadamente se cada ramo principal já recebeu ao menos uma pedra além da carroça
4. Liberar as duas laterais da carroça inicial somente quando ambos os ramos principais tiverem recebido pedras
5. Máximo 4 pontas simultâneas

**Estados da Mesa**:
```
EMPTY → ONE_END → TWO_ENDS → FOUR_ENDS (com laterais desbloqueadas)
```

**Exemplos**:
```python
board = Board()
board.is_empty()  # True

board.play_piece(Piece(6, 6), EndType.MAIN_LEFT)  # Carroça inicial
board.get_end_value(EndType.MAIN_LEFT)  # Naipe de encaixe: 6, não 12
board.is_lateral_unlocked()  # False

board.play_piece(Piece(6, 3), EndType.MAIN_LEFT)
board.play_piece(Piece(3, 2), EndType.MAIN_LEFT)
board.is_lateral_unlocked()  # False: direita ainda sem pedra adicional

board.play_piece(Piece(6, 4), EndType.MAIN_RIGHT)
board.is_lateral_unlocked()  # True: ambos os ramos receberam pedras
board.play_piece(Piece(6, 1), EndType.LATERAL_TOP)  # Encaixa no 6 inicial
board.get_end_value(EndType.LATERAL_TOP)  # 1
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
| consecutive_passes | int | Contador de passes seguidos desde a última jogada; o segundo não pontua |
| last_playing_player_id | Optional[int] | Autor da última jogada; recebe novamente a vez após passe geral |
| pass_sequence_score | dict[int, int] | Pontos de passe atribuídos por dupla na sequência atual, a substituir pelo total de 50 se ocorrer passe geral |
| last_playing_pair_id | Optional[int] | Dupla da última jogada válida; recebe os 50 pontos do galo |
| initial_five_doubles_decision | Optional[bool] | None = aguardando decisão do jogador com 5 carroças; True = aceita; False = recusa |
| state | RoundState | Estado atual da raia |
| winner_pair_id | Optional[int] | ID da dupla vencedora (se encerrada) |

**Métodos**:
| Método | Retorna | Descrição |
|--------|---------|-----------|
| `start() -> None` | None | Inicia raia (distribui pedras) |
| `play_piece(piece: Piece) -> Score` | Score | Executa jogada e retorna pontuação |
| `pass_turn() -> dict[int, int]` | dict | Retorna ajustes de placar por dupla: passe comum 20, segundo passe 0, passe geral total 50 com reversão dos pontos de passe da sequência |
| `check_end_conditions() -> Optional[RoundEndReason]` | RoundEndReason or None | Verifica batida/tranca; galo é evento durante a raia |
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
| TRANCA | Jogo bloqueado (sem jogadas possíveis) |

**Condições de Término**:
1. **BATIDA**: Jogador joga última pedra (hand vazia). Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez.
2. **TRANCA**: Nenhum dos quatro jogadores tem jogada válida.

**Evento durante a raia — passe geral (galo)**: O passe vale 20 pontos para a dupla adversária; o segundo passe consecutivo não pontua. Quando os outros três jogadores passam após uma jogada e seu autor tem jogada disponível, ocorre galo (passe geral): a sequência vale somente 50 pontos para a dupla da última jogada, sem acumular os 20 pontos de passe. A raia continua e a vez retorna ao jogador que fez a última jogada. O evento não altera `RoundState` para um estado terminal. Se os quatro jogadores passam, é jogo fechado (tranca), não galo: a raia termina e não há bônus de 50 pontos de passe geral. O galo exige que o autor da última jogada possa jogar novamente após os passes dos outros três.

---

### Cálculo da contagem final da raia

Na tranca e na batida normal (sem carroça final), a dupla vencedora recebe a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo: `pontos = (soma_adversária // 5) * 5`. Somar as duas mãos antes de arredondar; não incluir a mão do parceiro nem subtrair a soma da dupla vencedora. O resultado é creditado ao placar da dupla vencedora.

Se as somas das mãos das duas duplas forem iguais na tranca, nenhuma dupla recebe pontos por essa tranca, independentemente de quem jogou por último. Comparar as somas antes de qualquer arredondamento e preservar o placar já acumulado. Nesse caso, `winner_pair_id = None` e `scores_awarded = {0: 0, 1: 0}`. A batida com carroça segue a exceção de 20 pontos mais as pontas, sem contar mãos adversárias.

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
| `check_match_victory() -> Optional[int]` | int or None | Verifica vitória por pontuação após batida/tranca e contagem final; durante a raia, atingir 200 não basta |
| `is_finished() -> bool` | bool | True quando o estado da partida é FINISHED; não apenas por atingir 200 durante a raia |
| `get_winner() -> Optional[int]` | int or None | ID da dupla vencedora |
| `get_scoreboard() -> dict` | dict | Mapa {pair_id: score} |

**Estados (MatchState)**:
| Estado | Descrição |
|--------|-----------|
| INIT | Partida não iniciada |
| IN_PROGRESS | Raias sendo jogadas |
| FINISHED | Partida encerrada (vencedor definido) |

**Regras**:
- Vitória ao atingir >= 200 pontos ao final de uma raia; vitória automática também ocorre se um jogador receber 7 carroças na distribuição inicial
- Após batida, quem bateu inicia a próxima raia. Após tranca, quem receber o 6-6 inicia com essa pedra.
- Com exatamente 6 carroças na mão inicial, o jogador joga normalmente. Com 7 carroças na mão inicial de um jogador, sua dupla vence a partida automaticamente. A opção de recusa e o bônus de 50 pontos aplicam-se somente a exatamente 5 carroças.
- Cinco carroças iniciais exigem decisão de aceitar ou recusar pelo jogador; somente a aceitação concede 50 pontos à sua dupla. Se recusar, todos devolvem as 28 pedras, que são embaralhadas e distribuídas novamente (7 por jogador), sem conceder o bônus de 50 pontos. A decisão pertence à distribuição atual e deve ser reiniciada após a redistribuição.
- Partida pode ter múltiplas raias
- Se, após batida ou jogo fechado e a contabilização final da raia, os placares acumulados das duas duplas forem iguais e de 200 pontos ou mais, jogar outra raia, preservando o placar. Repetir enquanto houver empate ao fim da raia; não encerrar no primeiro desempate durante a raia. A abertura segue a regra do encerramento anterior: após batida, o batido; após tranca, quem receber o 6-6.

---

## Enums

### RoundState
```python
class RoundState(Enum):
    INIT = auto()
    DEALT = auto()
    IN_PROGRESS = auto()
    BATIDA = auto()
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
    winner_pair_id: int | None  # None em tranca empatada
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
