# Plano de Implementação: Domino Amazonense

**Feature Branch**: `001-dominio-amazonense`

**Plano Criado**: 2026-09-30

**Status**: Draft

---

## Contexto Técnico

### Tecnologias Selecionadas

| Camada | Tecnologia | Motivo |
|--------|------------|--------|
| Linguagem | Python 3.12 | Especificado pelo usuário, suporte moderno a type hints |
| Testes | pytest | Padrão da indústria, fixtures poderosas, coverage integrado |
| Interface | Web para navegador no computador | Frontend integrado ao motor Python; framework a definir |
| Validação | Pydantic v2 | Validação de dados com type hints, integração pytest |
| Linting | ruff + mypy | Formatação rápida e type checking estrito |

### Arquitetura Proposta

```
src/domino/
├── domain/              # Camada de Domínio (regras de negócio)
│   ├── entities/       # Entidades imutáveis
│   │   ├── piece.py    # Peça do dominó
│   │   ├── player.py   # Jogador
│   │   ├── pair.py     # Dupla
│   │   └── board.py    # Mesa (estrutura de 4 pontas)
│   ├── value_objects/  # Value objects
│   │   └── score.py    # Valor de pontuação
│   ├── events/         # Eventos de domínio
│   │   └── game_events.py
│   └── __init__.py
├── application/        # Camada de Aplicação (casos de uso)
│   ├── use_cases/      # Casos de uso específicos
│   │   ├── start_game.py
│   │   ├── play_piece.py
│   │   ├── pass_turn.py
│   │   └── calculate_round.py
│   ├── services/       # Serviços de aplicação
│   │   ├── scorer.py   # Lógica de pontuação progressiva
│   │   ├── validator.py # Validação de jogadas
│   │   └── game_state.py # Gerenciamento de estado
│   └── __init__.py
├── infrastructure/     # Camada de Infraestrutura
│   ├── repositories/   # Persistência (se necessária)
│   ├── generators/     # Geradores de peças, embaralhamento
│   └── __init__.py
└── gui/                # Apresentação gráfica PyQt6
    ├── main.py         # Janela e entry point
    ├── controllers.py  # Integração com casos de uso
    └── widgets.py      # Mesa e pedras

tests/
├── domain/             # Testes de domínio
│   ├── entities/
│   ├── value_objects/
│   └── events/
├── application/        # Testes de aplicação
│   ├── use_cases/
│   └── services/
├── infrastructure/     # Testes de infraestrutura
└── interface/          # Testes de interface
```

---

## Verificação da Constituição

### Princípios Fundamentais

| Princípio | Status | Observações |
|-----------|--------|-------------|
| I. Python 3.11+ | ✓ ADEQUADO | User especificou Python 3.12 |
| II. Mesa de Bar | ✓ PLANEJADO | GUI com mesa e pedras desde a primeira versão |
| III. Clean Architecture | ✓ PLANEJADO | Arquitetura em camadas definida |
| III. Testes Primeiros | ✓ PLANEJADO | TDD com pytest, 80% coverage mínimo |
| IV. Arquitetura Modular | ✓ PLANEJADO | Módulos independentes definidos |
| V. Documentação ADRs | ✓ A fazer | Criar ADRs durante implementação |

### Regras do Jogo - Compliance

| Regra | FR Correspondente | Status |
|-------|-------------------|--------|
| 4 jogadores, 2 duplas | FR-005, FR-006 | ✓ Definido |
| Pontuação múltiplo de 5 | FR-003, FR-004 | ✓ Definido |
| Sistema progressivo 4 pontas | FR-002, FR-003 | ✓ Definido |
| Ramos laterais condicionais | FR-005 | ✓ Definido |
| Passe = 20 pontos | FR-006 | ✓ Definido |
| Passe geral = somente 50 pontos à última dupla; retorna ao último jogador sem encerrar raia | FR-007, FR-008 | ✓ Definido |
| Batida normal: soma adversária arredondada para baixo em múltiplos de 5 | FR-009, FR-010 | ✓ Definido |
| Vitória 200+ pontos verificada após batida/tranca e contagem final | FR-011 | ✓ Definido |
| Tranca compara mãos; vencedora recebe soma adversária arredondada para baixo em múltiplos de 5 | FR-012, FR-013 | ✓ Definido |
| 5 carroças: aceitação concede 50 pontos à dupla; recusa causa novo embaralhamento e distribuição das 28 pedras sem bônus | FR-016 | ✓ Definido |
| 6 carroças = jogo normal; 7 carroças na mão de um jogador = vitória automática da dupla | FR-017, FR-017.1 | ✓ Definido |

---

## Gates de Qualidade

### Pré-Implementação

- [ ] Especificação aprovada
- [ ] Plano de implementação revisado
- [ ] Ambiguidades resolvidas (Clarify completo)

### Pós-Design (Phase 1)

- [ ] data-model.md documenta todas as entidades
- [ ] research.md resolve todas as incertezas técnicas
- [ ] quickstart.md define fluxo de validação

### Pós-Implementação

- [ ] Todos os testes passando
- [ ] Coverage ≥ 80%
- [ ] Linting zero erros
- [ ] ADRs documentados

---

## Fase 0: Pesquisa

### Incertezas Técnicas a Resolver

**NEEDS RESEARCH** (já resolvido pelo agente de pesquisa):
- ✅ Estrutura de dados para mesa com 4 pontas progressivas
- ✅ Algoritmo de validação de jogadas com ramos laterais
- ✅ Padrão de implementação para pontuação progressiva
- Interface web para computador definida; framework do frontend a definir

**Decisões do agente de pesquisa** (IMPLEMENTATION_FINDINGS.md):
1. **GUI Framework**: Interface web para computador; frontend a definir; protótipo PyQt6 substituído no plano de entrega
2. **Board Model**: Graph com EndType enum (MAIN_LEFT, MAIN_RIGHT, LATERAL_TOP, LATERAL_BOTTOM)
3. **Scoring**: ProgressiveScorer com eventos de domínio
4. **GUI**: controles visuais ligados aos casos de uso, com domínio independente

---

## Fase 1: Design e Contratos

### Entidades de Domínio (data-model.md)

#### Pedra (Piece)
- **Fields**: lado_a (0-6), lado_b (0-6)
- **Validations**: valores inteiros 0-6, imutável
- **Methods**: is_doble(), flip(), matches(value)
- **Events**: PiecePlayed

#### Mesa (Board)
- **Fields**: extremidades (dict EndType → value), pedras_jogadas (list)
- **Validations**: máximo 4 pontas, laterais ancoradas na carroça inicial e liberadas somente após uma pedra adicional em cada ramo principal
- **Methods**: play_piece(piece, target_end), get_available_ends()
- **State**: EMPTY → ONE_END → TWO_ENDS → FOUR_ENDS

#### Jogador (Player)
- **Fields**: id, nome, mao (list[Piece])
- **Validations**: máximo 7 pedras iniciais
- **Methods**: has playable_piece(board), play(piece), pass_turn()

#### Dupla (Pair)
- **Fields**: id, jogadores (list[Player]), pontos (int)
- **Methods**: add_points(), get_total_hand_points()

#### Partida (Match)
- **Fields**: duplas (list[Pair]), raia_atual (int), estado (enum)
- **Validations**: vitória ≥ 200 pontos
- **Methods**: start_round(), next_round(), is_winner()

#### Raia (Round)
- **Fields**: board, turno_atual, histórico_jogadas, estado
- **States**: INICIADA, EM_ANDAMENTO, BATIDA, TRANCA
- **Methods**: play_piece(), pass_turn(), check_end_conditions()

### Transições de Estado

```
Partida:
  INIT → INICIADA (start)
  INICIADA → EM_ANDAMENTO (first piece)
  EM_ANDAMENTO → BATIDA/TRANCA (end conditions)
  BATIDA/TRANCA → RESULTADO (score calculated)
  RESULTADO → INICIADA (nenhuma dupla atingiu 200 ou placares acumulados empatados em 200+)
  RESULTADO → FINALIZADA (winner declared)

Raia:
  INIT → INICIADA (deal pieces)
  INICIADA → EM_ANDAMENTO (first play)
  EM_ANDAMENTO → BATIDA (player empties hand)
  EM_ANDAMENTO → EM_ANDAMENTO (passe geral: outros três passam; somente 50 pontos; último jogador joga novamente)
  EM_ANDAMENTO → TRANCA (blocked, no more plays)
```

### Contratos de Interface Gráfica

- Selecionar pedra e ponta visualmente e executar o caso de uso de jogada.
- Exibir mesa, turno, placar das duplas e eventos recebidos do motor.
- Oferecer controles de nova partida, passe e decisão de cinco carroças.
- Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.
- Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

### Validação da GUI

Implementar frontend e serviço web, validar acesso por navegador e testar uma partida completa pela tela. A GUI atual é um protótipo, sem integração suficiente para esse fluxo.

---

## Plano de Implementação (Tasks)

### Iteração 1: Núcleo de Domínio

**Objetivo**: Entidades básicas funcionais com testes

- [ ] `domain/entities/piece.py` - Classe Piece com validação
- [ ] `domain/entities/player.py` - Classe Player com mão
- [ ] `domain/entities/pair.py` - Classe Pair para duplas
- [ ] `domain/entities/board.py` - Classe Board com estrutura de 4 pontas
- [ ] `tests/domain/entities/` - Testes para todas as entidades
- [ ] `domain/events/game_events.py` - Eventos base

**Critério de Aceite**: 
- Piece valida valores 0-6, detecta dobles
- Player tem mão inicial, verifica jogabilidade
- Board aceita peças válidas, atualiza pontas
- Pair soma pontos corretamente

### Iteração 2: Lógica de Pontuação

**Objetivo**: Sistema de pontuação progressiva

- [ ] `domain/entities/score.py` - Value object Score
- [ ] `application/services/scorer.py` - ProgressiveScorer
- [ ] `application/services/validator.py` - MoveValidator
- [ ] `tests/application/services/test_scorer.py` - Testes progressivos
- [ ] `tests/application/services/test_validator.py` - Testes de validação

**Critério de Aceite**:
- Pontuação 1 peça = valor da peça
- Pontuação 2 peças = soma das 2 pontas
- Pontuação 4 peças = soma das 4 pontas
- Pontuação só marca em múltiplo de 5

### Iteração 3: Casos de Uso

**Objetivo**: Fluxo completo de jogo

- [ ] `application/use_cases/start_game.py` - StartGame
- [ ] `application/use_cases/play_piece.py` - PlayPiece
- [ ] `application/use_cases/pass_turn.py` - PassTurn
- [ ] `application/use_cases/calculate_round.py` - CalculateRoundScore
- [ ] `application/services/game_state.py` - GameStateManager
- [ ] `tests/application/use_cases/` - Testes de integração

**Critério de Aceite**:
- Game inicia com embaralhamento e distribuição
- PlayPiece valida e executa jogada
- PassTurn aplica passe comum de 20, segundo passe de 0 ou passe geral de somente 50 pontos conforme a sequência
- CalculateRound detecta batida/tranca; passe geral é tratado durante a raia

### Iteração 4: Condições de Término

**Objetivo**: Finalização de raias e partidas

- [ ] `application/use_cases/check_batida.py` - BatidaDetector
- [ ] `application/use_cases/check_galo.py` - GaloDetector
- [ ] `application/use_cases/check_tranca.py` - TrancaResolver
- [ ] `application/use_cases/check_victory.py` - VictoryChecker
- [ ] `tests/application/use_cases/test_end_conditions.py`

**Critério de Aceite**:
- Batida detecta hand vazia
- Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez.
- Batida normal e tranca: somar as duas mãos adversárias e arredondar o total para baixo em múltiplos de 5; excluir a mão do parceiro e não usar diferença de mãos
- Passe comum vale 20; segundo passe consecutivo vale 0
- Galo exige que o autor da última jogada possa jogar novamente após os passes dos outros três jogadores; totaliza somente 50 pontos para a última dupla que jogou e retorna ao mesmo jogador sem encerrar a raia
- Quatro jogadores sem jogada: jogo fechado (tranca), sem bônus de galo
- Após tranca, a próxima raia começa com quem receber o 6-6, jogando essa pedra
- Tranca compara somas brutas das mãos por dupla; em igualdade, nenhuma dupla pontua e o placar acumulado permanece inalterado
- Vitória por pontuação verifica ≥ 200 somente após batida/tranca e contagem final; atingir a meta durante a raia não interrompe o jogo

### Iteração 5: Infraestrutura

**Objetivo**: Geradores e utilitários

- [ ] `infrastructure/generators/piece_generator.py` - Gera 28 peças
- [ ] `infrastructure/generators/shuffler.py` - Embaralhamento
- [ ] `infrastructure/generators/dealer.py` - Distribuição inicial
- [ ] `tests/infrastructure/` - Testes de geradores

**Critério de Aceite**:
- Generator cria todas 28 peças (0-0 a 6-6)
- Shuffler usa Fisher-Yates ou equivalente
- Dealer distribui 7 peças cada, aleatoriamente

### Iteração 6: Interface Gráfica

**Objetivo**: Jogo completo pela tela, pelo navegador no computador.

- [ ] Implementar frontend web e API/serviço de sessão ligados ao motor Python
- [ ] Implementar mesa, pedras, seleção de ponta, passe e placar
- [ ] Oferecer decisão de cinco carroças e transição entre raias
- [ ] Validar interação, renderização e execução após instalação

**Critério de Aceite**: Partida completa operada por controles visuais, com regras aplicadas pelo motor e atualização de turno, mesa e placar.

### Iteração 7: Polish e Documentação

**Objetivo**: Qualidade e documentação

- [ ] ADRs criados para decisões arquiteturais
- [ ] README.md com instruções de uso
- [ ] Docstrings completas
- [ ] ruff e mypy passing
- [ ] Coverage report ≥ 80%

---

## Métricas de Sucesso

| Métrica | Alvo | Como Medir |
|---------|------|------------|
| Coverage | ≥ 80% | pytest --cov |
| Linting | 0 errors | ruff check |
| Type Checking | 0 errors | mypy src/ |
| Testes Unitários | 100+ testes | pytest -v |
| Performance | < 200ms/jogada | benchmark script |

---

## Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Complexidade da estrutura de 4 pontas | Alto | Prototipar Board primeiro, testar extensivamente |
| Regras de ramos laterais | Médio | Documentar fluxos com diagramas, validar com regras oficiais |
| Detecção de galo/tranca | Médio | Testes de integração com cenários completos |
| Integração entre motor e GUI | Baixo | Manter domain/application independentes de interface |

---

## Próximos Passos

1. **Criar estrutura de diretórios** conforme arquitetura acima
2. **Implementar Iteração 1** (entidades básicas) com TDD
3. **Executar testes** após cada entidade
4. **Revisar e iterar** antes de prosseguir para próxima iteração

## Integração dos participantes

- O jogador entra escolhendo um apelido, sem cadastro, login ou senha. No multiplayer, pode criar uma sala ou informar o código de uma sala existente. Manter sessão anônima para reconexão, separada do nome de exibição.

- Durante a partida, se um jogador humano perder a conexão, um jogador controlado pelo computador assume seu lugar, preservando mão, dupla e estado da partida. Cada jogada tem limite de 20 segundos. Ao esgotar os 20 segundos, o computador executa uma jogada válida pelo jogador naquele turno. Se não houver jogada válida, executa o passe conforme as regras do jogo. Para um humano ainda conectado, essa ação automática não transfere permanentemente o controle ao computador. Após reconectar, o humano retoma sua mesma posição no início do próximo turno que lhe couber, preservando mão, dupla e estado atual. A reconexão não desfaz jogadas já realizadas pelo computador nem interrompe o turno em andamento.

- O multiplayer começa pela criação de uma sala. A sala reúne quatro jogadores humanos, cada um no navegador de seu computador, para uma partida em duas duplas. Ao criar a sala, o sistema gera e exibe um código. Os demais jogadores entram informando esse código na interface web. No multiplayer, os próprios jogadores escolhem suas duplas na sala antes do início da partida. Cada dupla deve ter exatamente dois jogadores; a partida só pode começar com as duas duplas completas. As duplas permanecem fixas durante a partida. Quando os quatro jogadores estiverem na sala e houver exatamente dois em cada dupla, o sistema embaralha e distribui automaticamente as 28 pedras, sete por jogador, sem comando do criador da sala. Aplicam-se as regras de cinco, seis e sete carroças antes da primeira jogada; na primeira raia, quem receber o 6-6 inicia jogando essa pedra.

- Implementar adaptadores de participante humano e computador sobre os mesmos casos de uso.
- Planejar uma autoridade única para validar jogadas e distribuir o estado público e as mãos privadas no multiplayer. Dispositivos definidos: computadores com navegador. Transporte e hospedagem ainda precisam ser definidos.
- Não considerar rede ou IA implementadas pelo protótipo gráfico existente.
