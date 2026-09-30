# Feature Specification: Domino Amazonense

**Feature Branch**: `001-dominio-amazonense`

**Created**: 2026-09-30

**Status**: Draft

**Input**: aplicação de dominó amazonense para 4 jogadores em 2 duplas, com regras de validação de jogada, contagem de pontos e condições de vitória

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Jogar uma pedra válida na mesa (Priority: P1)

Como jogador, quero poder jogar pedras válidas na mesa seguindo as regras do dominó amazonense, para participar ativamente da partida.

**Why this priority**: Esta é a funcionalidade central do jogo - sem validação de jogadas, o jogo não funciona. É o fluxo principal que todos os jogadores executarão repetidamente.

**Independent Test**: Pode ser testado validando que uma pedra é jogável ao verificar se algum lado combina com as pontas da mesa

**Acceptance Scenarios**:

1. **DADO** que existem pedras na mesa com pontas 4 e 6, **QUANDO** o jogador joga uma pedra com um lado 4, **ENTÃO** a pedra é aceita e as pontas são atualizadas
2. **DADO** que o jogador não tem pedras jogáveis, **QUANDO** ele tenta jogar uma pedra incompatível, **ENTÃO** o sistema rejeita a jogada e informa que deve passar
3. **DADO** que é o início do jogo, **QUANDO** o jogador possui o doble 6-6, **ENTÃO** ele deve começar a partida jogando essa pedra

---

### User Story 2 - Marcar pontos quando as pontas somam múltiplo de 5 (Priority: P1)

Como jogador, quero que o sistema marque pontos automaticamente quando as quatro pontas do jogo somarem um múltiplo de 5, para seguir as regras oficiais do dominó amazonense.

**Why this priority**: A pontuação é essencial para determinar o vencedor e é uma regra específica do dominó amazonense que diferencia este jogo de outras variações.

**Independent Test**: Pode ser testado simulando jogadas que resultam em soma das pontas igual a 10, 15, 20, etc., e verificando que os pontos são marcados corretamente

**Acceptance Scenarios**:

1. **DADO** que as quatro pontas da mesa somam 10, **QUANDO** uma pedra é jogada, **ENTÃO** a dupla que jogou marca 10 pontos
2. **DADO** que as quatro pontas somam 15, **QUANDO** uma pedra é jogada, **ENTÃO** a dupla que jogou marca 15 pontos
3. **DADO** que as quatro pontas somam 7, **QUANDO** uma pedra é jogada resultando em soma 12, **ENTÃO** nenhum ponto é marcado (não é múltiplo de 5)

---

### User Story 3 - Passar quando não há jogada disponível (Priority: P2)

Como jogador, quero poder passar a vez quando não tenho pedras compatíveis para jogar, inclusive no início do jogo, para seguir o fluxo natural da partida.

**Why this priority**: O passe é uma mecânica essencial que permite o jogo continuar quando um jogador não pode agir, mas é menos crítico que as jogadas válidas.

**Independent Test**: Pode ser testado verificando que ao passar, a dupla adversária recebe 20 pontos e a vez muda

**Acceptance Scenarios**:

1. **DADO** que o jogador não tem pedras compatíveis com as pontas, **QUANDO** ele passa, **ENTÃO** a dupla adversária marca 20 pontos e a vez muda
2. **DADO** que é o início do jogo e o jogador não tem 6-6 nem pedras para começar, **QUANDO** ele passa, **ENTÃO** a dupla adversária marca 20 pontos
3. **DADO** que TODOS os jogadores passam em sequência, **QUANDO** ocorre o "galo", **ENTÃO** a dupla adversária marca 50 pontos automaticamente
4. **DADO** que o jogador tem pedras jogáveis, **QUANDO** ele tenta passar, **ENTÃO** o sistema rejeita o passe e anuncia vitória da dupla adversária

---

### User Story 4 - Bater e esvaziar a mão (Priority: P1)

Como jogador, quero poder vencer a raia jogando todas as minhas pedras até esvaziar a mão, para ganhar pontos da dupla adversária.

**Why this priority**: A batida é o objetivo principal de cada raia e determina a pontuação final da rodada.

**Independent Test**: Pode ser testado simulando um jogador que consegue jogar todas as 7 pedras até não ter mais nenhuma

**Acceptance Scenarios**:

1. **DADO** que o jogador tem apenas 1 pedra na mão, **QUANDO** ele joga essa pedra, **ENTÃO** ele bate e a raia termina
2. **DADO** que o jogador bate, **QUANDO** a raia termina, **ENTÃO** são contadas as pedras restantes dos adversários para pontuação
3. **DADO** que o jogador bate com uma carroça (doble) como última pedra, **QUANDO** ocorre a batida, **ENTÃO** recebe bônus de 20 pontos adicionais
4. **DADO** que o jogador bate com a pedra nas duas pontas simultaneamente ("Lá e Lô"), **QUANDO** ocorre a batida, **ENTÃO** aplica-se o bônus adicional

---

### User Story 5 - Encerrar partida ao atingir 200 pontos (Priority: P2)

Como jogador, quero que o sistema verifique automaticamente quando uma dupla atinge 200 pontos ou mais ao final de uma raia, para determinar o vencedor da partida.

**Why this priority**: A condição de vitória define quando a partida termina, mas só é verificada após o fim de cada raia, tornando-a menos frequente que as ações anteriores.

**Independent Test**: Pode ser testado simulando múltiplas raias até que uma dupla atinja 200+ pontos

**Acceptance Scenarios**:

1. **DADO** que uma dupla tem 180 pontos e termina uma raia batendo, **QUANDO** são somados os pontos da raia resultando em 210, **ENTÃO** a dupla vence a partida e o jogo encerra
2. **DADO** que uma dupla atinge 205 pontos mas a raia ainda não terminou, **QUANDO** a raia continua, **ENTÃO** o jogo só verifica a vitória após alguém bater
3. **DADO** que nenhuma dupla atingiu 200 pontos, **QUANDO** uma raia termina, **ENTÃO** o jogo continua para a próxima raia

---

### User Story 6 - Jogo fechado (tranca) com menos pontos na mão (Priority: P3)

Como jogador, quero que o sistema determine o vencedor de uma raia travada quem tem menos pontos nas pedras restantes, para lidar com situações de jogo fechado.

**Why this priority**: O cenário de tranca é menos comum que a batida normal, mas necessário para completar as regras do jogo.

**Independent Test**: Pode ser testado simulando uma situação onde nenhum jogador consegue jogar e todos passaram

**Acceptance Scenarios**:

1. **DADO** que o jogo está travado e ninguém pode mais jogar, **QUANDO** todos passaram, **ENTÃO** ganha quem tem menos pontos na mão
2. **DADO** que há empate de pontos na mão de tranca, **QUANDO** ocorre o empate, **ENTÃO** perde quem jogou por último
3. **DADO** que a raia terminou em tranca, **QUANDO** contam-se os pontos, **ENTÃO** a dupla com menos pontos marca a diferença

---

## Clarifications

### Session 2026-09-30

- Q: Como funciona o sistema de "4 pontas" para pontuação? → A: Pontuação sempre soma 4 pontas; não preenchidas valem 0. Início: carroça única (soma = soma dos dois lados da carroça, ex: 6-6 = 12). 2ª pedra: soma = carroça + ponta jogada. 3ª/4ª pedras (laterais): soma = pontas opostas + laterais (0 se vazias). 5ª+: soma completa das 4 pontas. Somente após 2 pontas preenchidas outros jogadores podem criar ramos laterais. Só marca pontos se a soma for múltiplo de 5.
- Q: A aplicação é para quantos jogadores? → A: 4 jogadores divididos em 2 duplas, conforme regras oficiais do dominó amazonense.
- Q: Qual é o valor do dobro 0 (bola/ovo) para pontuação? → A: Valor 0, não tem valor especial - é uma carroça como qualquer outra.
- Q: Como funciona a resolução de tranca e empates? → A: Maior soma de pontos na mão perde. A diferença é repassada como pontos para a dupla vencedora. Se ambas as duplas já tiverem 200+ pontos e empatarem na tranca, joga-se mais uma raia. Empates subsequentes permanecem até desempatar. Se a diferença não for múltiplo de 5, arredonda-se para baixo. Em caso de empate total de pontos nas duas duplas, nenhuma dupla pontua e segue para próxima raia.
- Q: Quem começa a primeira raia quando ninguém tem 6-6? → A: Isso não acontece - o 6-6 sempre será distribuído aleatoriamente entre os 4 jogadores no início, e quem recebe o 6-6 começa.
- Q: Como funciona quem inicia cada raia? → A: Primeira raia: quem tem o 6-6 inicia. Raias posteriores: quem bateu na raia anterior inicia a próxima. Se o batido não tiver carroça para iniciar (passou na raia anterior), a vez é para o próximo jogador na sequência.

---

## Edge Cases

- O que acontece quando um jogador inicia com 5 carroças? → Ganha 50 pontos imediatos
- O que acontece quando um jogador inicia com 6 carroças? → Vitória imediata da partida
- Como é determinado quem começa em raias posteriores? → Quem bateu na última rodada inicia; se não tiver carroça para iniciar (passou), vez passa para o próximo
- Como funciona o dobro 0 (bola/ovo)? → Valor 0, sem valor especial - trata-se como carroça normal
- Como funciona a resolução de tranca e empates? → Maior soma de pontos na mão perde. A diferença é repassada como pontos para a dupla vencedora. Se ambas as duplas já tiverem 200+ pontos e empatarem na tranca, joga-se mais uma raia. Empates subsequentes permanecem até desempatar. Se a diferença não for múltiplo de 5, arredonda-se para baixo. Em caso de empate total de pontos nas duas duplas, nenhuma dupla pontua.
- Quem começa a primeira raia? → Quem recebe o 6-6 na distribuição inicial (aleatória entre os 4 jogadores)
- O que acontece se jogador passa tendo jogada válida? → Sistema rejeita passe e dupla adversária vence imediatamente

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validar se uma pedra pode ser jogada comparando com as pontas da mesa
- **FR-001.1**: System MUST exigir que jogador especifique a ponta alvo ao jogar (ex: "play 3-5 LEFT")
- **FR-001.2**: System MUST detectar e impedir passe se jogador tiver jogada válida disponível
- **FR-002**: System MUST somar as pontas da mesa para pontuação: início (carroça única = seu valor), 2ª pedra (carroça + ponta), 3ª/4ª pedras (laterais valem 0 se vazias), 5ª+ pedras (4 pontas completas)
- **FR-003**: System MUST marcar pontos apenas quando soma das pontas (incluindo zeros de lados vazios) for múltiplo de 5
- **FR-004**: System MUST calcular pontos como igual à soma quando divisível por 5
- **FR-005**: System MUST permitir ramos laterais apenas após 2 pontas principais preenchidas
- **FR-005**: System MUST permitir passe quando jogador não tem pedras jogáveis
- **FR-006**: System MUST marcar 20 pontos para a dupla adversária quando um jogador passa
- **FR-007**: System MUST detectar "galo" quando todos os jogadores passam em sequência
- **FR-008**: System MUST marcar 50 pontos automaticamente em caso de galo
- **FR-009**: System MUST detectar batida quando jogador joga sua última pedra
- **FR-010**: System MUST contar pedras restantes dos adversários ao final de raia por batida
- **FR-010.5**: System MUST conceder bônus de 20 pontos quando jogador bate com carroça (doble) como última pedra
- **FR-011**: System MUST verificar vitória da partida ao final de cada raia quando dupla atinge 200+ pontos
- **FR-012**: System MUST resolver tranca comparando soma conjunta de pontos nas mãos de cada dupla (maior soma perde)
- **FR-013**: System MUST transferir diferença de pontos da dupla perdedora para a vencedora em caso de tranca (arredondar para baixo se não for múltiplo de 5)
- **FR-014**: System MUST determinar início da partida com jogador que recebe o 6-6 na distribuição aleatória das 28 pedras
- **FR-015**: System MUST determinar início de raias posteriores com quem bateu na rodada anterior. Se o batido não tiver carroça para iniciar, a vez passa para o próximo jogador na sequência.
- **FR-016**: System MUST verificar bonus de 50 pontos quando jogador inicia com 5 carroças
- **FR-017**: System MUST verificar vitória imediata quando jogador inicia com 6 carroças
- **FR-018**: System MUST jogar raia extra se ambas duplas ≥200 pontos e empatarem em tranca
- **FR-019**: System MUST continuar raias extras até desempatar empate em tranca com ambas ≥200 pontos
- **FR-020**: System MUST distribuir 28 pedras aleatoriamente entre 4 jogadores (7 pedras cada) no início

### Key Entities *(include if feature involves data)*

- **Pedra**: Peça do dominó com dois lados (0-6), inclui dobles (carroças)
- **Mesa**: Representação das pedras jogadas com suas pontas atuais
- **Jogador**: Participante da partida com mão de 7 pedras
- **Dupla**: Par de jogadores que jogam juntos e somam pontos
- **Partida**: Sessão completa de jogo disputada até 200+ pontos
- **Raia**: Rodada individual que termina com batida ou tranca
- **Pontuação**: Sistema de marcação em múltiplos de 5 e contagem de pedras

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das jogadas válidas são aceitas em menos de 200ms
- **SC-002**: 100% das jogadas inválidas são rejeitadas com mensagem clara ao usuário
- **SC-003**: Pontuação é calculada corretamente em 100% dos cenários de múltiplos de 5
- **SC-004**: Partidas podem ser completadas do início ao fim sem intervenção manual
- **SC-005**: Sistema detecta corretamente batida, galo e tranca em 100% dos casos
- **SC-006**: Usuários conseguem jogar uma partida completa de dominó amazonense seguindo as regras oficiais

## Assumptions

- Usuários têm familiaridade básica com regras de dominó
- A aplicação será implementada primeiro em Python conforme constituição do projeto
- Interface gráfica não está incluída nesta especificação inicial (foco em lógica de negócio)
- Jogadores individuais são agrupados em duplas fixas durante toda a partida
- O conjunto de pedras é o duplo-6 (28 pedras totais)
- O jogo evolui no sentido anti-horário (tradicional no Amazonas)
