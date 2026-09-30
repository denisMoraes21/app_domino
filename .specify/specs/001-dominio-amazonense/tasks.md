---
description: "Task list para implementação do Domino Amazonense"
---

# Tasks: Domino Amazonense

**Input**: Design documents from `/specs/001-dominio-amazonense/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Abordagem**: TDD com pytest (80% coverage mínimo)

**Organização**: Tasks por user story para implementação independente

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configuração inicial do projeto Python com TDD

- [ ] T001 Criar estrutura de diretórios per arquitetura: `src/domino/{domain, application, infrastructure, interface}/` e `tests/{domain, application, infrastructure, interface}/`
- [ ] T002 Criar `pyproject.toml` com metadata do projeto e configurações de ferramentas
- [ ] T003 Criar `requirements.txt` com dependências: pytest>=7.4.0, pytest-cov>=4.1.0, pydantic>=2.0.0, ruff>=0.1.0, mypy>=1.7.0
- [ ] T004 [P] Criar `.gitignore` padrão Python
- [ ] T005 [P] Criar `README.md` com descrição inicial do projeto

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Configurações de qualidade e estrutura base

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Criar `.env.example` com variáveis de ambiente básicas (se aplicável)
- [ ] T007 [P] Configurar `ruff.toml` com regras estritas para Python 3.12
- [ ] T008 [P] Configurar `mypy.ini` ou seção mypy em `pyproject.toml` com strict mode
- [ ] T009 [P] Configurar `pytest.ini` com addopts para verbose, coverage, e fail-under 80
- [ ] T010 Criar `src/domino/__init__.py` com versão do projeto (ex: `__version__ = "0.1.0"`)
- [ ] T011 Criar `tests/__init__.py` para tornar tests pacote Python
- [ ] T012 Criar `conftest.py` na raiz de tests com fixtures base (board vazio, peça padrão, jogadores de teste)

---

## Phase 3: User Story 1 - Jogar uma pedra válida na mesa (Priority: P1) MVP

**Goal**: Validar que pedras podem ser jogadas na mesa seguindo regras do dominó amazonense

**Independent Test**: Pode ser testado validando que uma pedra é jogável ao verificar se algum lado combina com as pontas da mesa

### Tests for User Story 1

- [ ] T013 [P] [US1] Criar `tests/domain/entities/test_piece.py` com testes para Piece: is_doble, matches, get_matching_side, flip, total, validação 0-6
- [ ] T014 [P] [US1] Criar `tests/domain/entities/test_board.py` com testes para Board: is_empty, play_piece, get_end_value, get_available_ends, evolução 1→2→4 pontas
- [ ] T015 [P] [US1] Criar `tests/application/services/test_validator.py` com testes para MoveValidator: can_play com diferentes cenários de pontas
- [ ] T016 [US1] Criar teste de integração para fluxo completo: jogador joga pedra válida → pedra aceita → pontas atualizadas em `tests/application/use_cases/test_play_piece.py`

### Implementation for User Story 1

- [ ] T017 [P] [US1] Implementar entidade `Piece` em `src/domino/domain/entities/piece.py` com side_a, side_b (0-6), is_doble(), matches(), get_matching_side(), flip(), total()
- [ ] T018 [P] [US1] Implementar enum `EndType` em `src/domino/domain/entities/board.py` com MAIN_LEFT, MAIN_RIGHT, LATERAL_TOP, LATERAL_BOTTOM
- [ ] T019 [P] [US1] Implementar entidade `Board` em `src/domino/domain/entities/board.py` com _ends dict, _pieces_played, play_piece(), get_end_value(), get_available_ends(), is_lateral_unlocked()
- [ ] T020 [US1] Implementar `MoveValidator` em `src/domino/application/services/validator.py` com can_play(piece, board, target_end) retornando (bool, str)
- [ ] T021 [P] [US1] Criar value object `Score` em `src/domino/domain/value_objects/score.py` com validação value >= 0 e método is_multiple_of_5()
- [ ] T022 [US1] Criar eventos de domínio em `src/domino/domain/events/game_events.py`: PiecePlayedEvent com player_id, piece, target_end, board_state, scored, points_earned

**Checkpoint**: US1 completa - pedra pode ser jogada e validada

---

## Phase 4: User Story 2 - Marcar pontos quando pontas somam múltiplo de 5 (Priority: P1)

**Goal**: Sistema de pontuação progressiva baseado nas 4 pontas da mesa

**Independent Test**: Simular jogadas resultando em soma 10, 15, 20 e verificar pontos marcados corretamente

### Tests for User Story 2

- [ ] T023 [P] [US2] Criar `tests/application/services/test_scorer.py` com testes para ProgressiveScorer: 1 peça (carroça única), 2 peças (carroça + ponta), 3-4 peças (laterais vazias), 5+ peças (4 pontas completas)
- [ ] T024 [P] [US2] Criar testes de integração em `tests/application/use_cases/test_scoring.py` simulando sequência de jogadas com múltiplos de 5
- [ ] T025 [P] [US2] Criar testes para edge cases: soma 0 (bola/ovo), soma não múltipla de 5 (sem pontos), laterais vazias valem 0

### Implementation for User Story 2

- [ ] T026 [P] [US2] Implementar `ProgressiveScorer` em `src/domino/application/services/scorer.py` com método calculate_score(board) retornando soma baseada na fase do jogo
- [ ] T027 [US2] Adicionar método `should_score(total: int)` em `ProgressiveScorer` verificando total % 5 == 0
- [ ] T028 [US2] Integrar scoring no fluxo de jogada: após play_piece, calcular score, verificar should_score, marcar pontos se aplicável
- [ ] T029 [US2] Adicionar registro de evento ScoredEvent em `game_events.py` quando pontos são marcados

**Checkpoint**: US2 completa - pontuação progressiva funcionando com múltiplos de 5

---

## Phase 5: User Story 3 - Passar quando não há jogada disponível (Priority: P2)

**Goal**: Permitir passe quando jogador não tem pedras jogáveis, marcando 20 pontos para adversários

**Independent Test**: Ao passar, verificar que dupla adversária recebe 20 pontos e vez muda

### Tests for User Story 3

- [ ] T030 [P] [US3] Criar `tests/application/use_cases/test_pass_turn.py` com testes para: passe válido sem jogáveis, passe inválido com jogáveis, passe resulta em 20 pontos para adversários
- [ ] T031 [P] [US3] Criar testes para detecção de galo: 4 passes consecutivos → 50 pontos

### Implementation for User Story 3

- [ ] T032 [P] [US3] Implementar entidade `Player` em `src/domino/domain/entities/player.py` com id, name, pair_id, hand, has_playable_piece(board), get_playable_pieces(board), play(piece, target_end), pass_turn(), get_hand_value(), add_piece(piece)
- [ ] T033 [P] [US3] Implementar entidade `Pair` em `src/domino/domain/entities/pair.py` com id, players (2 jogadores), total_score, add_points(points), get_total_hand_points(), has_playable_piece(board)
- [ ] T034 [US3] Implementar `PassTurn` use case em `src/domino/application/use_cases/pass_turn.py` retornando pontos concedidos (20) e validando se jogador tem jogável disponível (caso contrário, vitória adversária)
- [ ] T035 [US3] Implementar `GaloDetector` em `src/domino/application/use_cases/check_galo.py` com registro de passes consecutivos e detecção quando >= 4
- [ ] T036 [US3] Integrar detecção de galo: após cada passe, verificar galo, aplicar 50 pontos se detectado
- [ ] T037 [US3] Adicionar TurnPassedEvent em `game_events.py` com player_id, is_galo, points_awarded

**Checkpoint**: US3 completa - passe e galo funcionando

---

## Phase 6: User Story 4 - Bater e esvaziar a mão (Priority: P1)

**Goal**: Detectar quando jogador esvazia a mão e calcular pontos da raia

**Independent Test**: Jogador com 1 pedra joga última pedra → batida detectada → pedras adversárias contadas

### Tests for User Story 4

- [ ] T038 [P] [US4] Criar `tests/application/use_cases/test_batida.py` com testes para: batida com última pedra, batida com "Lá e Lô" (doble nas duas pontas), contagem de pedras restantes
- [ ] T039 [P] [US4] Criar testes para cálculo de pontos da raia: batida normal, batida com doble final, contagem de pontos adversários

### Implementation for User Story 4

- [ ] T040 [P] [US4] Implementar `BatidaDetector` em `src/domino/application/use_cases/check_batida.py` com método has_batida(player) verificando hand vazia
- [ ] T041 [P] [US4] Implementar lógica de batida especial em `BatidaDetector`: detectar bônus de 20 pontos quando último jogo é carroça (doble)
- [ ] T042 [US4] Implementar `CalculateRoundScore` em `src/domino/application/use_cases/calculate_round.py` contando pedras restantes dos adversários e calculando pontos
- [ ] T043 [US4] Adicionar BatidaEvent em `game_events.py` com player_id, piece, round_points, adversaries_hand_values
- [ ] T044 [US4] Integrar verificação de batida após cada jogada válida

**Checkpoint**: US4 completa - batida e contagem de pontos funcionando

---

## Phase 7: User Story 5 - Encerrar partida ao atingir 200 pontos (Priority: P2)

**Goal**: Verificar vitória da partida ao final de cada raia quando dupla atinge 200+ pontos

**Independent Test**: Dupla com 180 pontos bate resultando em 210 → vitória detectada e partida encerrada

### Tests for User Story 5

- [ ] T045 [P] [US5] Criar `tests/application/use_cases/test_victory.py` com testes para: vitória ao atingir 200+, vitória ao exceder 200, partida continua abaixo de 200
- [ ] T046 [P] [US5] Criar testes para múltiplas raias até vitória

### Implementation for User Story 5

- [ ] T047 [P] [US5] Implementar entidade `Round` em `src/domino/domain/entities/round.py` com board, current_player_id, players, play_history, consecutive_passes, state (enum), winner_pair_id
- [ ] T048 [P] [US5] Implementar entidade `Match` em `src/domino/domain/entities/match.py` com pairs (2), current_round, state, rounds_played, first_batida_pair_id
- [ ] T049 [P] [US5] Implementar enum `RoundState` em `src/domino/domain/entities/round.py` com INIT, DEALT, IN_PROGRESS, BATIDA, GALO, TRANCA
- [ ] T050 [P] [US5] Implementar enum `MatchState` em `src/domino/domain/entities/match.py` com INIT, IN_PROGRESS, FINISHED
- [ ] T051 [P] [US5] Implementar enum `RoundEndReason` em `src/domino/domain/entities/round.py` com BATIDA, GALO, TRANCA
- [ ] T052 [US5] Implementar `VictoryChecker` em `src/domino/application/use_cases/check_victory.py` verificando >= 200 pontos ao final de raia
- [ ] T053 [US5] Implementar `Match.start()` e `Match.start_next_round()` para gerenciar fluxo de raias
- [ ] T054 [US5] Adicionar RoundEndedEvent e MatchEndedEvent em `game_events.py`
- [ ] T055 [US5] Integrar verificação de vitória após cálculo de pontos de cada raia

**Checkpoint**: US5 completa - vitória da partida funcionando

---

## Phase 8: User Story 6 - Jogo fechado (tranca) com menos pontos na mão (Priority: P3)

**Goal**: Resolver tranca comparando pontos nas mãos das duplas (maior soma perde)

**Independent Test**: Jogo travado → todos passaram → ganha quem tem menos pontos → diferença transferida para vencedor

### Tests for User Story 6

- [ ] T056 [P] [US6] Criar `tests/application/use_cases/test_tranca.py` com testes para: tranca normal (maior soma perde), tranca empatada (último a jogar perde), diferença arredondada para baixo
- [ ] T057 [P] [US6] Criar testes para tranca com ambas duplas >= 200 pontos exigindo raia extra
- [ ] T058 [P] [US6] Criar testes para diferença de pontos não múltipla de 5 (arredondamento para baixo)

### Implementation for User Story 6

- [ ] T059 [P] [US6] Implementar `TrancaResolver` em `src/domino/application/use_cases/check_tranca.py` comparando soma conjunta de pontos nas mãos de cada dupla
- [ ] T060 [US6] Implementar lógica de empate em tranca: quem jogou por último (última jogada válida antes dos passes) perde
- [ ] T061 [US6] Implementar lógica de arredondamento: se diferença não for múltipla de 5, arredondar para baixo
- [ ] T062 [US6] Implementar lógica de raia extra: se ambas duplas >= 200 e empatarem em tranca, iniciar nova raia imediatamente
- [ ] T063 [US6] Adicionar TrancaEvent em `game_events.py` com winning_pair_id, losing_pair_hand_value, points_transferred
- [ ] T064 [US6] Integrar detecção de tranca: após galo sem batida, chamar TrancaResolver

**Checkpoint**: US6 completa - tranca e empates resolvidos

---

## Phase 9: Infrastructure (Geradores e Distribuição)

**Purpose**: Criar 28 pedras, embaralhar e distribuir aleatoriamente

- [ ] T065 [P] Implementar `PieceGenerator` em `src/domino/infrastructure/generators/piece_generator.py` gerando todas 28 pedras (0-0 a 6-6)
- [ ] T066 [P] Implementar `Shuffler` em `src/domino/infrastructure/generators/shuffler.py` com Fisher-Yates shuffle
- [ ] T067 [US1] Implementar `Dealer` em `src/domino/infrastructure/generators/dealer.py` distribuindo 7 pedras aleatoriamente para cada jogador
- [ ] T068 [US5] Implementar lógica de distribuição inicial: identificar quem tem 6-6 e definir como primeiro jogador
- [ ] T069 [US5] Implementar lógica de distribuição para raias posteriores: quem bateu na raia anterior inicia

---

## Phase 10: Special Cases (5/6 carroças iniciais)

**Purpose**: Bônus e vitória imediata para carroças iniciais

- [ ] T070 [P] Implementar verificação de 5 carroças iniciais em `src/domino/application/use_cases/check_initial_bonus.py` → 50 pontos imediatos
- [ ] T071 [P] Implementar verificação de 6 carroças iniciais em `src/domino/application/use_cases/check_initial_bonus.py` → vitória imediata da partida
- [ ] T072 Adicionar InitialBonusEvent em `game_events.py` com player_id, caroca_count, bonus_points

---

## Phase 11: Interface CLI

**Purpose**: Interface interativa via terminal com argparse

- [ ] T073 Criar estrutura CLI em `src/domino/interface/cli/` com `__init__.py`, `main.py`, `commands.py`, `formatters.py`
- [ ] T074 [P] [US1] Implementar `create_cli()` em `src/domino/interface/cli/main.py` com argparse configurando subcommands: start, play, pass, status, score, quit
- [ ] T075 [US1] Implementar `play_piece_command(piece_str)` em `src/domino/interface/cli/commands.py` parseando "X-Y" e chamando play_piece
- [ ] T076 [US3] Implementar `pass_command()` em `src/domino/interface/cli/commands.py` executando passe
- [ ] T077 [US1] Implementar `status_command()` em `src/domino/interface/cli/commands.py` mostrando estado da mesa (4 pontas) e pedras jogadas
- [ ] T078 [US2] Implementar `score_command()` em `src/domino/interface/cli/commands.py` mostrando pontuação por dupla e histórico
- [ ] T079 [US5] Implementar `start_command()` em `src/domino/interface/cli/commands.py` iniciando nova partida com distribuição
- [ ] T080 [US5] Implementar `quit_command()` em `src/domino/interface/cli/commands.py` mostrando pontuação final
- [ ] T081 [P] Implementar formatação de mesa em `src/domino/interface/cli/formatters.py` com visualização ASCII das 4 pontas
- [ ] T082 [P] Implementar formatação de mão do jogador em `src/domino/interface/cli/formatters.py` listando pedras disponíveis
- [ ] T083 [P] Implementar formatação de mensagens de evento em `src/domino/interface/cli/formatters.py` (batida, galo, tranca, pontos)
- [ ] T084 Criar `tests/interface/cli/test_commands.py` com testes de CLI (mockando lógica de domínio)
- [ ] T085 Criar `tests/interface/cli/test_formatters.py` com testes de formatação de saída

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Qualidade, documentação e validação final

- [ ] T086 [P] Adicionar docstrings para todas as classes e métodos públicos
- [ ] T087 [P] Adicionar type hints completos em todos os módulos Python
- [ ] T088 Rodar `ruff check src/` e corrigir todos os erros de linting
- [ ] T089 Rodar `mypy src/` e corrigir todos os erros de tipo
- [ ] T090 [P] Criar ADRs em `.specify/adr/` para decisões arquiteturais principais
- [ ] T091 Atualizar `README.md` com instruções completas de uso
- [ ] T092 Executar `pytest tests/ --cov=src/domino --cov-report=term-missing` e garantir >= 80% coverage
- [ ] T093 Executar cenários de validação do `quickstart.md` end-to-end
- [ ] T094 Criar script `.specify/scripts/run.sh` para iniciar CLI rapidamente
- [ ] T095 Criar script `.specify/scripts/test.sh` para rodar testes com coverage
- [ ] T096 Configurar pre-commit hooks em `.pre-commit-config.yaml` com ruff e mypy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sem dependências - pode começar imediatamente
- **Foundational (Phase 2)**: Depende de Setup - BLOQUEIA todas as user stories
- **User Stories (Phase 3-8)**: Todas dependem de Foundational completion
- **Infrastructure (Phase 9)**: Pode ser feita em paralelo com US1-US4
- **Special Cases (Phase 10)**: Depende de US1 (Piece entity) e US5 (Match entity)
- **CLI (Phase 11)**: Depende de todas as user stories completas
- **Polish (Phase 12)**: Depende de todas as outras fases

### User Story Dependencies

- **US1 (P1)**: Sem dependências - pode começar após Foundational
- **US2 (P1)**: Depende de US1 (Board e Piece entidades)
- **US3 (P2)**: Depende de US1 (Board) e Player entity
- **US4 (P1)**: Depende de US1-US3 (todas entidades e validação)
- **US5 (P2)**: Depende de US1-US4 (Round e Match entidades)
- **US6 (P3)**: Depende de US5 (Match e Round entities)
- **Infrastructure**: Pode rodar em paralelo com US1-US4
- **Special Cases**: Depende de US1 e US5
- **CLI**: Depende de todas as US

### Parallel Opportunities

- **Setup Phase**: T004, T005 podem rodar em paralelo
- **Foundational Phase**: T007-T012 podem rodar em paralelo
- **US1**: T013-T016 (tests) em paralelo; T017-T022 (impl) em paralelo
- **US2**: T023-T025 (tests) em paralelo; T026-T029 (impl) em paralelo
- **US3**: T030-T031 (tests) em paralelo; T032-T037 (impl) podem ser agrupados
- **US4**: T038-T039 (tests) em paralelo; T040-T044 (impl) podem ser agrupados
- **US5**: T045-T046 (tests) em paralelo; T047-T055 (impl) podem ser agrupados
- **US6**: T056-T058 (tests) em paralelo; T059-T064 (impl) podem ser agrupados
- **Infrastructure**: T065-T069 podem rodar em paralelo
- **Special Cases**: T070-T072 podem rodar em paralelo
- **CLI**: T084-T085 (tests) em paralelo; formatters (T081-T083) em paralelo
- **Polish**: T086-T087, T088-T089, T090-T096 podem ser agrupados

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**Foco**: US1 + US2 (jogar pedras e pontuação básica)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (jogar pedra válida)
4. Complete Phase 4: US2 (pontuação progressiva)
5. **STOP and VALIDATE**: Teste fluxo básico completo
6. Deploy/demo MVP funcional

### Incremental Delivery (Recomendado)

1. Phase 1-2: Foundation completa
2. Add US1: Joga pedra válida → testar independente
3. Add US2: Pontuação progressiva → testar independente
4. Add US4: Batida → testar independente
5. Add US3: Passe e galo → testar independente
6. Add US5: Vitória da partida → testar independente
7. Add US6: Tranca → testar independente
8. Add Infrastructure: Geradores completados
9. Add Special Cases: Bônus 5/6 carroças
10. Add CLI: Interface interativa
11. Polish: Linting, docs, coverage

### Parallel Team Strategy

Com múltiplos desenvolvedores:

1. Dev A: Setup + Foundational (foco em qualidade)
2. Dev B: US1 + US2 (core gameplay)
3. Dev C: US3 + US4 (passe, batida, galo)
4. Dev D: Infrastructure + US5 + US6
5. Todos: CLI colaborativa
6. Todos: Polish conjunto

---

## Task Checklist Summary

**Total Tasks**: 96

- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 7 tasks
- Phase 3 (US1 - Jogar pedra): 10 tasks
- Phase 4 (US2 - Pontuação): 7 tasks
- Phase 5 (US3 - Passe/Galo): 8 tasks
- Phase 6 (US4 - Batida): 5 tasks
- Phase 7 (US5 - Vitória): 9 tasks
- Phase 8 (US6 - Tranca): 7 tasks
- Phase 9 (Infrastructure): 5 tasks
- Phase 10 (Special Cases): 3 tasks
- Phase 11 (CLI): 13 tasks
- Phase 12 (Polish): 11 tasks

**Tasks with [P]**: ~45 tasks paralelizáveis
**Tasks with [US*]**: 96 tasks distribuídos por user stories

---

## Notes

- Abordagem TDD: escrever testes FIRST para cada fase de user story
- Tasks [P] podem rodar em paralelo sem conflitos
- Cada user story deve ser independente e testável isoladamente
- Coverage mínimo 80% obrigatório
- Linting e type checking estritos (ruff + mypy)
- Commit após cada tarefa ou grupo lógico
- Validar com quickstart.md ao final de cada fase principal
