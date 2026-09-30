# Feature Specification: Domino Simplex

**Feature Branch**: `002-dominio-simplex`

**Created**: 2026-09-30

**Status**: Draft

**Input**: aplicação de dominó para dois jogadores com peças tradicionais, embaralhar, distribuir, validar jogadas, comprar/passar, encerrar rodada e calcular pontuação

---

## Contexto

Esta especificação define uma aplicação de dominó simplificada para **2 jogadores** (não em duplas), seguindo as regras básicas do jogo tradicional com peças de duplo-6. O escopo concentra-se exclusivamente na **lógica de negócio**, sem decisões sobre interface gráfica, bibliotecas específicas ou persistência de dados.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Iniciar partida com embaralhamento e distribuição (Priority: P1)

Como jogador, quero que as 28 peças do dominó sejam embaralhadas e distribuídas igualmente (7 peças cada) no início da partida, para garantir aleatoriedade e justiça no jogo.

**Why this priority**: Esta é a pré-condição fundamental para qualquer partida. Sem distribuição correta, o jogo não pode começar.

**Independent Test**: Pode ser testado executando a inicialização e verificando que: (1) todas as 28 peças foram geradas, (2) o baralho foi embaralhado, (3) cada jogador recebeu exatamente 7 peças, (4) restaram 14 peças no bico

**Acceptance Scenarios**:

1. **DADO** que nenhuma partida está em andamento, **QUANDO** um jogador inicia nova partida, **ENTÃO** o sistema gera 28 peças (0-0 a 6-6), embaralha e distribui 7 para cada jogador
2. **DADO** que a distribuição ocorreu, **QUANDO** verificamos as mãos, **ENTÃO** Jogador 1 tem 7 peças, Jogador 2 tem 7 peças, e 14 peças permanecem no bico (não usadas nesta variação)
3. **DADO** que múltiplas partidas são iniciadas, **QUANDO** comparamos distribuições consecutivas, **ENTÃO** cada partida tem sequência de peças diferente devido ao embaralhamento

---

### User Story 2 - Jogar peça válida nas pontas da mesa (Priority: P1)

Como jogador, quero jogar uma peça da minha mão que combine com pelo menos uma das pontas expostas na mesa, para progredir no jogo.

**Why this priority**: A jogada é a ação central do jogo. Sem validação correta, as regras não são aplicadas e o jogo perde sentido.

**Independent Test**: Pode ser testado verificando que peças compatíveis são aceitas e incompatíveis são rejeitadas, com atualização correta das pontas

**Acceptance Scenarios**:

1. **DADO** que as pontas da mesa são [3] e [5], **QUANDO** o jogador joga a peça (3-4), **ENTÃO** a peça é aceita e as novas pontas passam a ser [4] e [5]
2. **DADO** que as pontas da mesa são [2] e [6], **QUANDO** o jogador joga a peça (6-6), **ENTÃO** a peça é aceita e a nova ponta é 12 (6+6)
3. **DADO** que as pontas da mesa são [1] e [4], **QUANDO** o jogador tenta jogar (2-5), **ENTÃO** o sistema rejeita a jogada com mensagem "Peça não compatível com as pontas"
4. **DADO** que é o início do jogo e mesa está vazia, **QUANDO** o jogador joga sua primeira peça, **ENTÃO** a peça é aceita e define as duas pontas iniciais

---

### User Story 3 - Passar quando não houver jogada possível (Priority: P2)

Como jogador, quero passar minha vez quando não tiver nenhuma peça compatível para jogar, para que o adversário possa continuar o jogo.

**Why this priority**: O passe é necessário quando o jogador está bloqueado, permitindo que o jogo avance. Não há compra de peças - as 14 peças restantes ficam no bico sem serem usadas nesta variação.

**Independent Test**: Pode ser testado simulando jogador sem jogadas válidas e verificando que o turno passa ao adversário sem penalidades

**Acceptance Scenarios**:

1. **DADO** que o jogador não tem peças compatíveis com as pontas, **QUANDO** ele passa, **ENTÃO** a vez muda para o adversário sem pontuação
2. **DADO** que ambos jogadores passam consecutivamente, **QUANDO** ocorre passagem dupla, **ENTÃO** o sistema detecta bloqueio mútuo e encerra a rodada
3. **DADO** que o jogador tem peças compatíveis, **QUANDO** tenta passar, **ENTÃO** o sistema rejeita e informa "Você tem jogada disponível"

---

### User Story 4 - Encerrar rodada por batida (Priority: P1)

Como jogador, quero que a rodada termine imediatamente quando eu zerar minhas peças, para determinar o vencedor daquela rodada.

**Why this priority**: A batida é uma das duas condições de vitória e representa o objetivo principal de cada jogador.

**Independent Test**: Pode ser testado simulando jogador que esvazia a mão e verificando que a rodada encerra corretamente

**Acceptance Scenarios**:

1. **DADO** que o jogador tem apenas 1 peça na mão, **QUANDO** ele joga essa última peça, **ENTÃO** o sistema detecta batida e encerra a rodada imediatamente
2. **DADO** que ocorreu batida, **QUANDO** calcula-se a pontuação, **ENTÃO** o jogador vencedor ganha pontos equivalentes às peças restantes do adversário
3. **DADO** que o jogador bateu, **QUANDO** a rodada encerra, **ENTÃO** as pontuações são atualizadas e opcionalmente inicia-se nova rodada

---

### User Story 5 - Encerrar rodada por bloqueio mútuo (Priority: P2)

Como jogador, quero que a rodada termine quando ambos os jogadores estiverem bloqueados sem possibilidade de jogada, para resolver situações de empate técnico.

**Why this priority**: O bloqueio mútuo é a segunda condição de encerramento, garantindo que jogos travados não permaneçam infinitos.

**Independent Test**: Pode ser testado simulando situação onde ambos jogadores passaram e verificando que a rodada encerra com cálculo de pontuação

**Acceptance Scenarios**:

1. **DADO** que ambos jogadores passaram consecutivamente, **QUANDO** o sistema detecta bloqueio mútuo, **ENTÃO** a rodada encerra e calcula pontuação baseada nas mãos restantes
2. **DADO** que a rodada encerrou por bloqueio, **QUANDO** calcula-se o vencedor, **ENTÃO** ganha quem tem menos pontos nas peças restantes
3. **DADO** que há empate de pontos nas mãos, **QUANDO** ocorre empate no bloqueio, **ENTÃO** aplica-se regra de desempate: quem jogou por último perde

---

### User Story 6 - Calcular pontuação da rodada (Priority: P1)

Como jogador, quero que os pontos da rodada sejam calculados automaticamente ao final, para acompanhar o progresso da partida.

**Why this priority**: A pontuação é essencial para determinar o vencedor da partida e manter a competitividade do jogo.

**Independent Test**: Pode ser testado simulando rodadas com diferentes cenários de batida e bloqueio, verificando cálculos corretos

**Acceptance Scenarios**:

1. **DADO** que Jogador A bateu, **QUANDO** calcula-se pontuação, **ENTÃO** Jogador A ganha pontos = soma dos valores das peças restantes de Jogador B
2. **DADO** que ocorreu bloqueio mútuo, **QUANDO** calcula-se pontuação, **ENTÃO** ganha quem tem menos pontos na mão e a pontuação = diferença entre as mãos
3. **DADO** que há empate de pontos nas mãos no bloqueio, **QUANDO** ocorre empate, **ENTÃO** define-se perdedor por critério adicional (ex: última jogada)
4. **DADO** que a rodada foi pontuada, **QUANDO** acumulamos pontos, **ENTÃO** o vencedor da partida é quem atingir primeiro a meta estabelecida (ex: 100 pontos)

---

- **Edge Cases**:
- **Peça dupla (carroça)**: Nova ponta é soma dos dois lados (ex: 3-3 → 6)
- **Início da partida**: Quem tem 6-6 começa; sem 6-6, quem tem peça mais alta (6-5 > 5-5 > 6-4, etc.); empate → sorteio
- **Empate de pontuação**: Quem jogou por último perde em bloqueio empatado (critério definido)
- **Peças restantes**: Valor máximo possível de pontos numa batida (soma de todas peças do adversário)

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST gerar 28 peças do dominó duplo-6 (combinações de 0-0 a 6-6)
- **FR-002**: System MUST embaralhar aleatoriamente o conjunto completo de peças antes da distribuição
- **FR-003**: System MUST distribuir 7 peças para cada um dos 2 jogadores no início da partida
- **FR-004**: System MUST permitir inicialização de nova partida a qualquer momento, reiniciando estado
- **FR-005**: System MUST validar jogada verificando compatibilidade de pelo menos um lado da peça com uma das pontas expostas
- **FR-006**: System MUST aceitar peça em qualquer ponta válida (esquerda ou direita) quando ambas compatíveis
- **FR-007**: System MUST atualizar pontas da mesa após cada jogada válida
- **FR-008**: System MUST tratar peças duplas (ex: 3-3) como transversais onde a nova ponta é a soma dos dois lados (3+3=6)
- **FR-009**: System MUST permitir passagem de turno quando jogador não tem jogada válida
- **FR-010**: System MUST detectar bloqueio mútuo quando ambos jogadores passam consecutivamente
- **FR-011**: System MUST encerrar rodada imediatamente ao detectar batida ou bloqueio mútuo
- **FR-012**: System MUST calcular pontos da batida = soma dos valores das peças restantes do adversário
- **FR-013**: System MUST calcular pontos do bloqueio = diferença entre soma das mãos (ganha quem tem menos)
- **FR-014**: System MUST acumular pontuação entre rodadas para determinar vencedor da partida
- **FR-015**: System MUST definir meta de vitória (ex: 100 pontos) configurável

### Key Entities

- **Peça**: Elemento com dois valores (lado_a: 0-6, lado_b: 0-6), valores inteiros de 0 a 6; dobles (carroças) têm soma dos lados como nova ponta
- **Mesa**: Estrutura representando jogadas, com pontas esquerda e direita expostas
- **Jogador**: Entidade com identificador único e mão de peças (0-7 peças durante partida)
- **Partida**: Sessão completa com estado atual, jogadores, rodadas e pontuações acumuladas
- **Rodada**: Ciclo individual de jogo desde distribuição até batida ou bloqueio
- **Ponta**: Valor exposto em cada extremidade da mesa (esquerda e direita)

### Non-Functional Requirements

- **NFR-001**: Validação de jogada deve ocorrer em tempo real (< 100ms)
- **NFR-002**: Embaralhamento deve usar algoritmo de aleatoriedade adequada (ex: Fisher-Yates)
- **NFR-003**: Código deve seguir Clean Architecture conforme constitution do projeto
- **NFR-004**: Regras de negócio devem ser testáveis independentemente de UI/infraestrutura
- **NFR-005**: Type hints obrigatórios em todas as funções (Python 3.11+)
- **NFR-006**: Cobertura de testes mínima de 80% conforme constitution

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das jogadas válidas são aceitas corretamente
- **SC-002**: 100% das jogadas inválidas são rejeitadas com mensagem apropriada
- **SC-003**: Distribuição inicial sempre resulta em 7 peças por jogador com 28 peças totais (14 peças restantes não usadas)
- **SC-004**: Passe ocorre quando jogador não tem jogada válida
- **SC-005**: Passe é rejeitado quando jogador tem jogada disponível
- **SC-006**: Batida detectada imediatamente ao zerar mão (0 peças restantes)
- **SC-007**: Bloqueio mútuo detectado após 2 passes consecutivos
- **SC-008**: Cálculo de pontuação em batida = soma correta das peças adversárias
- **SC-009**: Cálculo de pontuação em bloqueio = diferença correta das mãos
- **SC-010**: Partida pode ser jogada do início ao fim sem intervenção manual
- **SC-011**: 100% da lógica de negócio coberta por testes automatizados

---

## Assumptions

- Aplicação será implementada em Python conforme constitution do projeto
- Interface gráfica será desenvolvida separadamente (esta especificação foca em lógica de negócio)
- Persistência de dados não está no escopo inicial (apenas estado em memória)
- Jogadores são locais (não há multiplayer remoto nesta fase)
- A pontuação do bloqueio segue regra: ganha quem tem menos pontos na mão
- Meta de vitória padrão é 100 pontos (pode ser configurada futuramente)
- Quem tem 6-6 inicia a primeira rodada; rodadas subsequentes iniciam com quem bateu
- Peças duplas (carroças) têm nova ponta = soma dos dois lados (ex: 3-3 → 6)
- Início: 6-6 primeiro; sem 6-6 → peça mais alta (6-5 > 5-5 > 6-4); empate → sorteio
- Desempate de bloqueio empatado: quem jogou por último perde
- Não há compra de peças - 14 peças restantes ficam no bico sem serem usadas

---

## Out of Scope

- Interface gráfica ou GUI (apenas lógica de negócio)
- Multiplayer remoto ou networking
- Persistência de partidas ou histórico
- Animações ou efeitos visuais
- Variações regionais específicas do dominó amazonense (foco em regras tradicionais simplificadas)
- IA ou bots oponentes
- Sistema de apostas ou fichas
- Placar gráfico ou dashboard
