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
| Interface | CLI (argparse) | Inicial simples, foco em lógica de negócio primeiro |
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
└── interface/          # Camada de Apresentação
    ├── cli/            # Interface de linha de comando
    │   ├── main.py     # Entry point
    │   ├── commands.py # Comandos do CLI
    │   └── formatters.py # Formatação de saída
    └── __init__.py

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
| II. Mesa de Bar | ⚠️ OUT_OF_SCOPE | UI gráfica fora do escopo inicial (CLI primeiro) |
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
| Galo = 50 pontos | FR-007, FR-008 | ✓ Definido |
| Batida esvazia mão | FR-009, FR-010 | ✓ Definido |
| Vitória 200+ pontos | FR-011 | ✓ Definido |
| Tranca compara pontos | FR-012, FR-013 | ✓ Definido |
| 5 carroças = 50 pontos | FR-016 | ✓ Definido |
| 6 carroças = vitória | FR-017 | ✓ Definido |

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
- ✅ Biblioteca CLI recomendada (argparse vs click vs typer)

**Decisões do agente de pesquisa** (IMPLEMENTATION_FINDINGS.md):
1. **GUI Framework**: PyQt6 com QSS (para fase futura de GUI)
2. **Board Model**: Graph com EndType enum (MAIN_LEFT, MAIN_RIGHT, LATERAL_TOP, LATERAL_BOTTOM)
3. **Scoring**: ProgressiveScorer com eventos de domínio
4. **CLI**: argparse para simplicidade inicial (sem dependências extras)

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
- **Validations**: máximo 4 pontas, ramos laterais só após 2 principais
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
- **States**: INICIADA, EM_ANDAMENTO, BATIDA, GALO, TRANCA
- **Methods**: play_piece(), pass_turn(), check_end_conditions()

### Transições de Estado

```
Partida:
  INIT → INICIADA (start)
  INICIADA → EM_ANDAMENTO (first piece)
  EM_ANDAMENTO → BATIDA/GALO/TRANCA (end conditions)
  BATIDA/GALO/TRANCA → RESULTADO (score calculated)
  RESULTADO → INICIADA (next round if < 200)
  RESULTADO → FINALIZADA (winner declared)

Raia:
  INIT → INICIADA (deal pieces)
  INICIADA → EM_ANDAMENTO (first play)
  EM_ANDAMENTO → BATIDA (player empties hand)
  EM_ANDAMENTO → GALO (all pass)
  EM_ANDAMENTO → TRANCA (blocked, no more plays)
```

### Contratos de Interface (CLI)

#### Comandos Principais
```
domino start      # Inicia nova partida
domino play <piece>  # Joga pedra (ex: "3-5")
domino pass       # Passa a vez
domino status     # Mostra estado atual
domino score      # Mostra pontuação
domino quit       # Encerra partida
```

#### Saída Formatada
- Estado da mesa: mostra 4 pontas com valores
- Mão do jogador: lista pedras disponíveis
- Pontuação: por dupla com histórico
- Validação: mensagens claras de erro

### Quickstart de Validação

**Pré-requisitos**:
```bash
python 3.12+ instalado
pip install pytest pydantic ruff mypy
```

**Setup**:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Executar testes**:
```bash
pytest tests/ --cov=src/domino --cov-report=term-missing
```

**Jogar partida de teste**:
```bash
python -m domino.interface.cli.main start
# Interagir via comandos CLI
```

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
- PassTurn marca 20 pontos para adversários
- CalculateRound detecta batida/galo/tranca

### Iteração 4: Condições de Término

**Objetivo**: Finalização de raias e partidas

- [ ] `application/use_cases/check_batida.py` - BatidaDetector
- [ ] `application/use_cases/check_galo.py` - GaloDetector
- [ ] `application/use_cases/check_tranca.py` - TrancaResolver
- [ ] `application/use_cases/check_victory.py` - VictoryChecker
- [ ] `tests/application/use_cases/test_end_conditions.py`

**Critério de Aceite**:
- Batida detecta hand vazia
- Galo detecta 4 passes consecutivos
- Tranca resolve empate por pontos na mão
- Vitória verifica ≥ 200 pontos

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

### Iteração 6: Interface CLI

**Objetivo**: Jogo jogável via terminal

- [ ] `interface/cli/main.py` - Entry point argparse
- [ ] `interface/cli/commands.py` - Comandos do CLI
- [ ] `interface/cli/formatters.py` - Formatação de saída
- [ ] `tests/interface/` - Testes de CLI
- [ ] `requirements.txt` - Dependências

**Critério de Aceite**:
- Comandos start, play, pass, status, score, quit
- Saída formatada legível
- Validação de input do usuário
- Mensagens de erro claras

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
| Balanceamento CLI vs futura GUI | Baixo | Manter domain/application independentes de interface |

---

## Próximos Passos

1. **Criar estrutura de diretórios** conforme arquitetura acima
2. **Implementar Iteração 1** (entidades básicas) com TDD
3. **Executar testes** após cada entidade
4. **Revisar e iterar** antes de prosseguir para próxima iteração
