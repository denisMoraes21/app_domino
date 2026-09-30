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

Domino Amazonense é um aplicativo gráfico em desenvolvimento do tradicional jogo de dominó praticado no Amazonas, onde **4 jogadores** divididos em **2 duplas** disputam com meta de **200 pontos**, verificando a vitória por pontuação somente ao final da raia.

Esta aplicação foi desenvolvida seguindo os princípios de **Clean Architecture** e **TDD (Test Driven Development)**, com cobertura de testes superior a 80%, garantindo confiabilidade e facilidade de manutenção.

### ⭐ Principais Características

- **Regras Oficiais do Dominó Amazonense**: Implementação fiel das regras tradicionais
- **Sistema de Pontuação Progressivo**: Soma das 4 pontas com múltiplos de 5
- **Detecção Automática**: Batida, Galo, Tranca e condições de vitória
- **Interface planejada**: mesa e pedras na tela, com controles visuais; acesso pelo navegador no computador
- **Arquitetura Limpa**: Separação clara entre domínio, aplicação, infraestrutura e interface
- **Código Testado**: Suite completa de testes com pytest
- **Type Safety**: Type hints completos com mypy
- **Código Limpo**: Linting estrito com ruff

---

## 🎮 Regras do Jogo

Há apenas um modo: **4 jogadores em 2 duplas**. A especificação Simplex foi retirada do escopo. As definições confirmadas pelo responsável pelo projeto prevalecem sobre referências divergentes.

### Visão Geral

- **Jogadores**: 4 jogadores em 2 duplas (Jogadores 0 e 2 vs Jogadores 1 e 3)
- **Pedras**: Conjunto duplo-6 (28 pedras, de 0-0 a 6-6)
- **Objetivo**: Alcançar 200 pontos ou mais; a vitória por pontuação é verificada somente após batida ou jogo fechado. Atingir a meta durante a raia não interrompe o jogo.
- **Direção**: Anti-horário (tradicional no Amazonas)

### Abertura das Laterais

As duas pontas laterais saem da carroça inicial. Só ficam disponíveis após jogar pelo menos uma pedra em cada uma das duas pontas principais; a carroça inicial não conta como preenchimento desses ramos. Jogar várias pedras apenas em uma ponta principal não libera as laterais. A primeira pedra de cada lateral deve combinar com o naipe da carroça inicial.

### Sistema de Pontuação

O jogo utiliza um **sistema progressivo de 4 pontas**:

| Fase | Pedras na Mesa | Cálculo | Pontos |
|------|----------------|---------|--------|
| 1ª pedra | 1 | Soma dos lados da carroça inicial (ex: 6-6 = 12) | Marca se múltiplo de 5 |
| 2ª pedra | 2 | Carroça + ponta jogada | Marca se múltiplo de 5 |
| 3ª/4ª pedra | 3-4 | Pontas opostas + laterais (0 se vazias) | Marca se múltiplo de 5 |
| 5ª+ pedra | 4 | Soma completa das 4 pontas | Marca se múltiplo de 5 |

**Regra importante**: Só marca pontos quando a soma é **múltiplo de 5** (5, 10, 15, 20...).

### Eventos e Condições de Término de Raia

#### Batida
- Ocorre quando um jogador joga sua **última pedra**
- Na batida normal (sem carroça final), a dupla que bateu recebe a soma das pedras restantes dos dois adversários, **arredondada para baixo ao múltiplo de 5 mais próximo**
- **Batida com carroça**: Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez.

#### Passe e Galo (Passe Geral)
- Passe comum: **20 pontos** para a dupla adversária.
- O **segundo passe consecutivo não pontua**.
- Se os outros três jogadores passam após uma jogada e seu autor consegue jogar novamente, ocorre o **galo**, ou passe geral.
- A sequência vale **somente 50 pontos** para a dupla da última jogada, sem acumular os 20 de passe.
- O galo **não encerra a raia**: quem jogou por último joga novamente.

#### Tranca (Jogo Fechado)
- Se os quatro jogadores passam, é jogo fechado (tranca), não galo: a raia termina e não há bônus de 50 pontos de passe geral. O galo exige que o autor da última jogada possa jogar novamente após os passes dos outros três.
- **Vence** quem tem **menos pontos** na mão (soma conjunta da dupla)
- A dupla vencedora recebe a **soma das mãos da dupla adversária**, arredondada para baixo ao múltiplo de 5 mais próximo
- Somam-se as duas mãos antes de arredondar: por exemplo, 18 + 19 = 37 → **35 pontos**
- Em caso de **igualdade na soma das mãos** das duplas, nenhuma recebe pontos pela tranca; o placar acumulado é preservado
- Empate das mãos não é empate de placar: o encerramento da partida depende do placar acumulado ao final da raia.

### Empate no Placar da Partida

Se, após batida ou jogo fechado e a contabilização final da raia, os placares acumulados das duas duplas forem iguais e de 200 pontos ou mais, jogar outra raia, preservando o placar. Repetir enquanto houver empate ao fim da raia; não encerrar no primeiro desempate durante a raia. A abertura segue a regra do encerramento anterior: após batida, o batido; após tranca, quem receber o 6-6.

### Regras Especiais

| Cenário | Regra |
|---------|-------|
| Exatamente 5 carroças iniciais | O jogador pode aceitar ou recusar jogar; se aceitar, sua dupla ganha **50 pontos** no início. Se recusar, recolhem-se as 28 pedras para novo embaralhamento e distribuição, sem bônus |
| 6 carroças iniciais | Joga normalmente |
| 7 carroças iniciais na mão de um jogador | Sua dupla vence a partida **automaticamente** |
| Dobro 0 (bola/ovo) | Valor 0, sem valor especial (carroça normal) |
| Quem inicia 1ª raia | Jogador com o **6-6** na distribuição |
| Quem inicia após batida | Quem **bateu** na raia anterior |
| Quem inicia após tranca | Quem receber a **carroça de sena (6-6)** inicia com ela |
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

## 🎮 Interface Web para Computador

O jogador entra escolhendo um apelido, sem cadastro, login ou senha. No multiplayer, pode criar uma sala ou informar o código de uma sala existente.

A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega.

A primeira versão será jogada na tela: mesa, pedras, pontas disponíveis, turno e placar das duas duplas. Os controles permitirão escolher solo ou criar/entrar em sala, selecionar pedra e ponta, passar e responder à opção de cinco carroças. No multiplayer, a distribuição começa automaticamente quando as duplas estão completas.

**Estado atual:** a GUI em `src/domino/gui/main.py` é um protótipo. A interface web ainda precisa ser criada e integrada ao motor; não há partida completa disponível. As instruções de execução serão validadas junto dessa integração.

Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.

Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

O multiplayer começa pela criação de uma sala. A sala reúne quatro jogadores humanos, cada um no navegador de seu computador, para uma partida em duas duplas. Ao criar a sala, o sistema gera e exibe um código. Os demais jogadores entram informando esse código na interface web. No multiplayer, os próprios jogadores escolhem suas duplas na sala antes do início da partida. Cada dupla deve ter exatamente dois jogadores; a partida só pode começar com as duas duplas completas. As duplas permanecem fixas durante a partida. Quando os quatro jogadores estiverem na sala e houver exatamente dois em cada dupla, o sistema embaralha e distribui automaticamente as 28 pedras, sete por jogador, sem comando do criador da sala. Aplicam-se as regras de cinco, seis e sete carroças antes da primeira jogada; na primeira raia, quem receber o 6-6 inicia jogando essa pedra.

Durante a partida, se um jogador humano perder a conexão, um jogador controlado pelo computador assume seu lugar, preservando mão, dupla e estado da partida. Cada jogada tem limite de 20 segundos. Ao esgotar os 20 segundos, o computador executa uma jogada válida pelo jogador naquele turno. Se não houver jogada válida, executa o passe conforme as regras do jogo. Para um humano ainda conectado, essa ação automática não transfere permanentemente o controle ao computador. Após reconectar, o humano retoma sua mesma posição no início do próximo turno que lhe couber, preservando mão, dupla e estado atual. A reconexão não desfaz jogadas já realizadas pelo computador nem interrompe o turno em andamento.

Plataforma definida: navegador no computador. Entrada definida por código da sala. Pendente: alcance da rede.

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
└── gui/                       # Camada de apresentação gráfica
    ├── main.py                # Janela e entry point PyQt6
    ├── controllers.py         # Integração planejada com casos de uso
    └── widgets.py             # Componentes planejados de mesa e pedras

tests/
├── domain/
├── application/
├── infrastructure/
└── gui/                       # Testes planejados de interação gráfica
```

A árvore acima é a arquitetura planejada; vários componentes ainda não existem.

---

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
