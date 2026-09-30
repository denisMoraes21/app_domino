# Quickstart: Domino Amazonense

**Criado**: 2026-09-30

**Objetivo**: Guiar validação rápida da implementação

---

## Pré-requisitos

- Python 3.12+ instalado
- pip ou poetry para gerenciamento de dependências
- Sistema operacional: Windows, macOS ou Linux

---

## Setup Inicial

### 1. Criar ambiente virtual

```bash
cd /home/denis/Documentos/GitHub/app_domino
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

**Dependências esperadas**:
```
# requirements.txt
pytest>=7.4.0
pytest-cov>=4.1.0
pydantic>=2.0.0
ruff>=0.1.0
mypy>=1.7.0
```

---

## Validar Implementação

### Testes Unitários

```bash
# Rodar todos os testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=src/domino --cov-report=term-missing

# Verificar se atinge 80% mínimo
pytest tests/ --cov=src/domino --cov-fail-under=80
```

**Saída esperada**:
```
============================= test session starts =============================
collected 100 items

tests/domain/entities/test_piece.py ...............                      [ 15%]
tests/domain/entities/test_board.py .....................                [ 36%]
tests/application/services/test_scorer.py ..................             [ 54%]
...
=================== 100 passed, 80.5% coverage in 0.42s ===================
```

### Linting e Type Checking

```bash
# Verificar style e erros
ruff check src/

# Verificar tipos
mypy src/
```

**Saída esperada**:
```
All 150 files checked. No errors found.
Success: no issues found in 150 files.
```

---

## Jogo Interativo via CLI

### Iniciar nova partida

```bash
python -m domino.interface.cli.main start
```

**Saída esperada**:
```
========================================
  Domino Amazonense
========================================
Nova partida iniciada!

Dupla A (Jogadores 0 e 2): 0 pontos
Dupla B (Jogadores 1 e 3): 0 pontos

Raia 1 - Sua vez!
Sua mão: [3-5, 6-6, 1-4, 2-2, 0-3, 5-5, 1-6]

Comandos:
  play <peça>  - Jogar pedra (ex: play 3-5)
  pass         - Passar a vez
  status       - Ver estado da mesa
  score        - Ver pontuação
  quit         - Sair
```

### Jogar pedra

```bash
play 3-5
```

**Saída esperada**:
```
Jogador 0 jogou 3-5 na ponta MAIN_LEFT
Mesa: [5] — [6-6] — [3]
Pontuação: Soma = 8 (não múltiplo de 5, sem pontos)
```

### Ver estado da mesa

```bash
status
```

**Saída esperada**:
```
Mesa Atual:
  Ponta Esquerda: 5
  Ponta Direita: 3
  Lateral Topo: (vazia)
  Lateral Base: (vazia)
  
Pedras jogadas: 2
Próximo jogador: Jogador 1
```

### Ver pontuação

```bash
score
```

**Saída esperada**:
```
Pontuação da Partida:
  Dupla A: 0 pontos
  Dupla B: 0 pontos

Últimos eventos:
  - Jogador 0: 3-5 (sem pontos)
```

### Passar a vez

```bash
pass
```

**Saída esperada**:
```
Jogador 0 passou a vez
Dupla adversária (B) marcou 20 pontos

Dupla A: 0 pontos
Dupla B: 20 pontos
```

### Verificar batida

```
Quando um jogador joga sua última pedra:

Jogador 2 jogou 1-1
BATIDA! Jogador 2 esvaziou a mão!

Raia terminada - Batida
Contagem de pedras restantes:
  Dupla A: 12 pontos
  Dupla B: 8 pontos
  
Pontos para Dupla A: 20 pontos
```

### Verificar galo

```
Quando todos passam consecutivamente:

Jogador 3 passou
Jogador 0 passou
Jogador 1 passou
Jogador 2 passou

GALO! Todos os jogadores passaram!
Dupla adversária marcou 50 pontos automaticamente
```

### Sair da partida

```bash
quit
```

**Saída esperada**:
```
Partida encerrada.
Pontuação final:
  Dupla A: 20 pontos
  Dupla B: 70 pontos
  
Obrigado por jogar!
```

---

## Cenários de Validação

### Cenário 1: Sistema progressivo de pontuação

1. Iniciar partida
2. Jogar carroça 6-6 → Soma = 6
3. Jogar 6-3 → Soma = 9 (6 + 3)
4. Jogar 3-2 → Soma = 11 (6 + 3 + 2 + 0)
5. Jogar 2-5 → Soma = 16 (6 + 3 + 2 + 5) → **15 pontos marcados!**

**Verificar**: A pontuação progressiva está correta em cada etapa.

### Cenário 2: Passe com penalidade

1. Iniciar partida
2. Jogador sem jogável passa
3. Verificar: Dupla adversária marca 20 pontos

### Cenário 3: Galo (todos passam)

1. Criar situação onde ninguém tem jogadas
2. Todos 4 jogadores passam consecutivamente
3. Verificar: Dupla adversária marca 50 pontos

### Cenário 4: Batida normal

1. Jogar até um jogador ter 1 pedra
2. Jogar última pedra
3. Verificar: Contagem de pedras adversárias e pontuação

### Cenário 5: Tranca (bloqueio)

1. Criar situação bloqueada sem galo
2. Sistema detecta tranca
3. Verificar: Quem tem menos pontos na mão vence

---

## Troubleshooting

### Testes falhando

```bash
# Verificar Python version
python --version  # Deve ser 3.12+

# Reinstalar dependências
pip uninstall -y pytest pytest-cov pydantic ruff mypy
pip install -r requirements.txt
```

### Coverage abaixo de 80%

```bash
# Verificar quais arquivos têm baixa cobertura
pytest tests/ --cov=src/domino --cov-report=html
open htmlcov/index.html
```

### Erros de type checking

```bash
# Verificar detalhes do erro
mypy src/ --show-error-codes
```

---

## Próximos Passos

Após validar o CLI básico:

1. **Testar cenários complexos**: 5 carroças iniciais, 6 carroças (vitória imediata)
2. **Validar ramos laterais**: Criar mesa com 4 pontas preenchidas
3. **Testar vitória da partida**: Atingir 200+ pontos
4. **Implementar GUI**: Migrar para PyQt6 com estilo "mesa de bar"

---

## Links de Referência

- [Especificação Funcional](./spec.md)
- [Modelo de Dados](./data-model.md)
- [Pesquisa Técnica](./research.md)
- [Plano de Implementação](./plan.md)
