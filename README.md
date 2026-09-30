# Domino Amazonense

<div align="center">

**Uma implementação moderna e completa do clássico dominó amazonense, seguindo as regras oficiais e as melhores práticas de desenvolvimento de software.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checking](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)

</div>

---

## 🎯 Sobre o Projeto

Domino Amazonense é uma implementação de linha de comando (CLI) do tradicional jogo de dominó praticado no Amazonas, onde **4 jogadores** divididos em **2 duplas** disputam até que uma delas atinja **200 pontos**.

Esta aplicação foi desenvolvida seguindo os princípios de **Clean Architecture** e **TDD (Test Driven Development)**, com cobertura de testes superior a 80%, garantindo confiabilidade e facilidade de manutenção.

### ⭐ Principais Características

- **Regras Oficiais do Dominó Amazonense**: Implementação fiel das regras tradicionais
- **Sistema de Pontuação Progressivo**: Soma das 4 pontas com múltiplos de 5
- **Detecção Automática**: Batida, Galo, Tranca e condições de vitória
- **Interface Intuitiva**: CLI amigável com feedback em tempo real
- **Arquitetura Limpa**: Separação clara entre domínio, aplicação, infraestrutura e interface
- **Código Testado**: Suite completa de testes com pytest
- **Type Safety**: Type hints completos com mypy
- **Código Limpo**: Linting estrito com ruff

---

## 🎮 Regras do Jogo

### Visão Geral

- **Jogadores**: 4 jogadores em 2 duplas (Jogadores 0 e 2 vs Jogadores 1 e 3)
- **Pedras**: Conjunto duplo-6 (28 pedras, de 0-0 a 6-6)
- **Objetivo**: Primeiro par a atingir 200 pontos ou mais vence a partida
- **Direção**: Anti-horário (tradicional no Amazonas)

### Sistema de Pontuação

O jogo utiliza um **sistema progressivo de 4 pontas**:

| Fase | Pedras na Mesa | Cálculo | Pontos |
|------|----------------|---------|--------|
| 1ª pedra | 1 | Soma dos lados da carroça inicial (ex: 6-6 = 12) | Marca se múltiplo de 5 |
| 2ª pedra | 2 | Carroça + ponta jogada | Marca se múltiplo de 5 |
| 3ª/4ª pedra | 3-4 | Pontas opostas + laterais (0 se vazias) | Marca se múltiplo de 5 |
| 5ª+ pedra | 4 | Soma completa das 4 pontas | Marca se múltiplo de 5 |

**Regra importante**: Só marca pontos quando a soma é **múltiplo de 5** (5, 10, 15, 20...).

### Condições de Término de Raia

#### Batida
- Ocorre quando um jogador joga sua **última pedra**
- A dupla adversária conta os pontos das pedras restantes na mão
- **Bônus especial**: +20 pontos se a última pedra for uma **carroça** (doble)

#### Galo
- Ocorre quando **todos os 4 jogadores** passam consecutivamente
- A dupla adversária marca **50 pontos** automaticamente

#### Tranca (Jogo Fechado)
- Ocorre quando nenhum jogador tem pedras jogáveis (sem passes consecutivos)
- **Vence** quem tem **menos pontos** na mão (soma conjunta da dupla)
- A diferença de pontos é transferida para a dupla vencedora
- Se a diferença não for múltipla de 5, **arredonda-se para baixo**
- Em caso de **empate total** entre as duplas: nenhuma pontua, segue para próxima raia
- Se ambas as duplas já tiverem **≥200 pontos** e empatarem: joga-se raia extra

### Regras Especiais

| Cenário | Regra |
|---------|-------|
| 5 carroças iniciais | Ganha **50 pontos** imediatos |
| 6 carroças iniciais | **Vitória imediata** da partida |
| Dobro 0 (bola/ovo) | Valor 0, sem valor especial (carroça normal) |
| Quem inicia 1ª raia | Jogador com o **6-6** na distribuição |
| Quem inicia raias seguintes | Quem **bateu** na raia anterior |
| Passe com jogada disponível | **Derrota imediata** para a dupla adversária |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- pip ou poetry para gerenciamento de dependências

### Passos

1. **Clone o repositório**

```bash
git clone https://github.com/denis-guimaraes/app_domino.git
cd app_domino
```

2. **Crie o ambiente virtual**

```bash
# Linux/macOS
python3.12 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

### Dependências

```
pytest>=7.4.0          # Framework de testes
pytest-cov>=4.1.0      # Coverage de testes
pydantic>=2.0.0        # Validação de dados
ruff>=0.1.0            # Linting rápido
mypy>=1.7.0            # Type checking
```

---

## 🎮 Como Jogar

### Iniciar uma Nova Partida

```bash
python -m domino.interface.cli.main start
```

### Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `play` | Jogar uma pedra na mesa | `play 3-5 LEFT` |
| `pass` | Passar a vez (quando sem jogada) | `pass` |
| `status` | Ver estado atual da mesa | `status` |
| `score` | Ver pontuação das duplas | `score` |
| `quit` | Encerrar a partida | `quit` |

### Exemplo de Jogo

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
  play <peça>  - Jogar pedra (ex: play 3-5 LEFT)
  pass         - Passar a vez
  status       - Ver estado da mesa
  score        - Ver pontuação
  quit         - Sair

>>> play 6-6 LEFT
Jogador 0 jogou 6-6 na ponta LEFT
Mesa: [12] (carroça inicial)
Pontuação: Soma = 12 (não múltiplo de 5, sem pontos)

>>> status
Mesa Atual:
  Ponta Esquerda: 6
  Ponta Direita: 6
  Lateral Topo: (vazia)
  Lateral Base: (vazia)
  
Pedras jogadas: 1
Próximo jogador: Jogador 1

>>> score
Pontuação da Partida:
  Dupla A: 0 pontos
  Dupla B: 0 pontos
```

---

## 🧪 Executar Testes

### Rodar Todos os Testes

```bash
pytest tests/ -v
```

### Com Coverage

```bash
pytest tests/ --cov=src/domino --cov-report=term-missing
```

### Validar Mínimo de 80%

```bash
pytest tests/ --cov=src/domino --cov-fail-under=80
```

### Verificar Linting

```bash
ruff check src/
```

### Verificar Tipos

```bash
mypy src/
```

---

## 🏗️ Arquitetura do Projeto

A aplicação segue os princípios da **Clean Architecture**, garantindo separação clara de responsabilidades e facilidade de teste.

```
src/domino/
├── domain/                     # Camada de Domínio (regras de negócio)
│   ├── entities/              # Entidades imutáveis
│   │   ├── piece.py          # Pedra do dominó (lado_a, lado_b)
│   │   ├── player.py         # Jogador com mão de pedras
│   │   ├── pair.py           # Par de jogadores (dupla)
│   │   └── board.py          # Mesa com 4 pontas progressivas
│   ├── value_objects/         # Value objects
│   │   └── score.py          # Valor de pontuação
│   ├── events/                # Eventos de domínio
│   │   └── game_events.py    # Eventos do jogo
│   └── __init__.py
├── application/               # Camada de Aplicação (casos de uso)
│   ├── use_cases/            # Casos de uso específicos
│   │   ├── play_piece.py     # Jugar pedra
│   │   ├── pass_turn.py      # Passar a vez
│   │   ├── check_batida.py   # Detecção de batida
│   │   ├── check_galo.py     # Detecção de galo
│   │   ├── check_tranca.py   # Resolução de tranca
│   │   ├── check_victory.py  # Verificação de vitória
│   │   └── calculate_round.py # Cálculo de pontos da raia
│   ├── services/             # Serviços de aplicação
│   │   ├── scorer.py         # Pontuação progressiva
│   │   └── validator.py      # Validação de jogadas
│   └── __init__.py
├── infrastructure/            # Camada de Infraestrutura
│   ├── generators/           # Geradores e distribuidores
│   │   ├── piece_generator.py # Gera 28 pedras
│   │   ├── shuffler.py       # Embaralhamento Fisher-Yates
│   │   └── dealer.py         # Distribuição inicial
│   └── __init__.py
└── interface/                 # Camada de Apresentação
    └── cli/                  # Interface de linha de comando
        ├── main.py           # Entry point com argparse
        ├── commands.py       # Comandos do CLI
        └── formatters.py     # Formatação de saída

tests/
├── domain/                   # Testes de domínio
├── application/              # Testes de aplicação
├── infrastructure/           # Testes de infraestrutura
└── interface/               # Testes de CLI
```

### Principais Entidades de Domínio

| Entidade | Responsabilidade |
|----------|------------------|
| **Piece** | Pedra do dominó (0-0 a 6-6), detecta dobles |
| **Player** | Jogador com mão de 7 pedras, verifica jogabilidade |
| **Pair** | Par de jogadores, pontuação compartilhada |
| **Board** | Mesa com evolução progressiva (1→2→4 pontas) |
| **Score** | Valor de pontuação validado (≥0) |
| **Round** | Raia individual com estado e histórico |
| **Match** | Partida completa com múltiplas raias |

---

## 📊 Métricas de Qualidade

| Métrica | Alvo | Ferramenta |
|---------|------|------------|
| Cobertura de testes | ≥ 80% | pytest-cov |
| Linting | 0 erros | ruff |
| Type checking | 0 erros | mypy |
| Testes unitários | 100+ | pytest |
| Performance | < 200ms/jogada | benchmark |

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Desenvolvimento

- Siga os princípios de Clean Architecture
- Escreva testes para todo novo código (TDD)
- Mantenha cobertura ≥ 80%
- Use type hints em todos os módulos
- Linting com ruff antes de commitar

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📚 Recursos

### Documentação

- [Especificação Funcional](.specify/specs/001-dominio-amazonense/spec.md)
- [Modelo de Dados](.specify/specs/001-dominio-amazonense/data-model.md)
- [Decisões Técnicas](.specify/specs/001-dominio-amazonense/research.md)
- [Plano de Implementação](.specify/specs/001-dominio-amazonense/plan.md)
- [Backlog de Tarefas](.specify/specs/001-dominio-amazonense/tasks.md)

### Sobre o Dominó Amazonense

O dominó amazonense é uma variação tradicional do jogo de dominó praticada no estado do Amazonas, Brasil. Diferente de outras variações, utiliza-se:

- 4 jogadores em 2 duplas fixas
- Sistema de pontuação progressivo com 4 pontas
- Regras específicas para tranca e empates
- Direção anti-horário no fluxo de jogo

---

## 🙏 Agradecimentos

- Comunidade brasileira de jogos de mesa tradicionais
- Python Software Foundation
- Mantenedores das bibliências: pytest, pydantic, ruff, mypy

---

<div align="center">

**Desenvolvido com ❤️ usando Python 3.12**

</div>
