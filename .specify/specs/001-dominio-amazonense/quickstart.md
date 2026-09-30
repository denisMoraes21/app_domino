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

## Jogo pela Interface Gráfica

A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega. O serviço web e o frontend ainda precisam ser implementados antes de validar uma partida completa.

Fluxo planejado de validação:

1. Acessar a aplicação pelo navegador de um computador e informar um apelido, sem cadastro ou senha.
2. Escolher solo ou multiplayer; no multiplayer, criar uma sala, compartilhar o código e reunir os demais participantes pela opção de entrada por código; cada jogador escolhe sua dupla e ao completar os quatro jogadores e as duas duplas, verificar embaralhamento e distribuição automáticos de sete pedras por jogador, sem botão de início; após resolver as regras de carroças iniciais, o portador do 6-6 faz a primeira jogada.
3. Selecionar uma pedra e a ponta de destino na mesa.
4. Conferir atualização da mesa, do turno e do placar.
5. Validar passe, decisão de cinco carroças e encerramento de raia pelos controles.
6. Completar a partida sem comandos de terminal.

Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.

Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

Validar uma partida solo e outra com quatro dispositivos. Os dispositivos serão computadores com navegador; o alcance da rede ainda será definido; rede e jogadores de computador não estão implementados.

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

### Cenário 3: Galo (passe geral)

1. Jogador 0 joga uma pedra e ainda pode jogar quando sua vez retornar
2. Os jogadores 1, 2 e 3 passam consecutivamente
3. Verificar: o segundo passe não pontua; a sequência inteira concede somente 50 pontos à dupla do jogador 0
4. Verificar: a raia continua, sem redistribuição, e o jogador 0 joga novamente

### Cenário 4: Batida normal

1. Jogar até um jogador ter 1 pedra
2. Jogar última pedra
3. Verificar: Somar as duas mãos adversárias antes de arredondar para baixo ao múltiplo de 5; 18 + 19 = 37 → 35 pontos de contagem

### Cenário 4b: Batida com carroça

1. Bater com carroça e soma das pontas de 10: total da jogada = 30 pontos (20 + 10)
2. Repetir sem pontuação nas pontas: total da jogada = 20 pontos
3. Em ambos os casos, não contar as mãos adversárias nem duplicar a pontuação das pontas

### Cenário 4c: Empate de placar e raia extra

1. Encerrar uma raia por batida ou tranca com placar acumulado 215–215
2. Verificar nova raia com o placar preservado e abertura conforme o encerramento anterior
3. Verificar que uma liderança durante a raia extra não encerra a partida
4. Se o placar empatar novamente ao fim da raia, verificar outra raia extra

### Cenário 5: Tranca (bloqueio)

1. Criar situação em que nenhum dos quatro jogadores consegue jogar
2. Os quatro passam: sistema detecta jogo fechado (tranca), sem conceder os 50 pontos de galo
3. Verificar: Quem tem menos pontos na mão vence e recebe a soma das mãos adversárias arredondada para baixo; totais 20 contra 37 → vencedora recebe 35 pontos
4. Repetir com somas iguais: nenhuma dupla pontua pela tranca e o placar acumulado permanece inalterado
5. Se a partida continuar, verificar que quem receber o 6-6 inicia a próxima raia com ele

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

Durante a integração da GUI:

1. **Testar cenários complexos**: 5 carroças iniciais (50 pontos para a dupla somente se o jogador aceitar jogar; se recusar, recolher as 28 pedras, embaralhar e distribuir 7 por jogador sem conceder o bônus), 6 carroças (jogo normal, sem bônus ou recusa), 7 carroças na mão de um jogador (vitória automática da dupla)
2. **Validar ramos laterais**: Abrir com 6-6; jogar 6-3 e 3-2 na esquerda mantém laterais bloqueadas; jogar 6-4 na direita libera as laterais; abrir uma delas com 6-1, usando o naipe da carroça inicial
3. **Testar vitória da partida**: Atingir 200+ durante a raia sem encerrá-la; verificar vitória por pontuação somente após batida ou tranca e contabilização final
4. **Validar GUI**: Completar uma partida na tela com o motor integrado

---

## Links de Referência

- [Especificação Funcional](./spec.md)
- [Modelo de Dados](./data-model.md)
- [Pesquisa Técnica](./research.md)
- [Plano de Implementação](./plan.md)

## Validar tempo e desconexão

- Conferir contador de 20 segundos a cada turno.
- Desconectar um participante durante uma partida e verificar que o computador assume sua posição, mão e dupla, sem reiniciar a partida.
- Deixar o prazo expirar: verificar jogada automática válida ou passe obrigatório se não houver jogada. O humano conectado mantém controle nos turnos seguintes.
- Reconectar o humano: verificar retomada no próximo turno que lhe couber, com a mão atual e sem desfazer jogadas do computador; conferir que somente o controlador vigente pode agir.
