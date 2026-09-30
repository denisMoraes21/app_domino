# Feature Specification: Domino Amazonense

**Feature Branch**: `001-dominio-amazonense`

**Created**: 2026-09-30

**Status**: Draft — único modo ativo; regras parcialmente esclarecidas

**Escopo vigente**: apenas 4 jogadores em 2 duplas. A especificação 002-Simplex foi retirada do escopo. Definições explícitas do responsável pelo projeto prevalecem sobre trechos divergentes das referências.

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

**Independent Test**: Pode ser testado verificando passe comum de 20 pontos, segundo passe consecutivo sem pontuação e passe geral de somente 50 pontos com retorno ao último jogador

**Acceptance Scenarios**:

1. **DADO** que o jogador não tem pedras compatíveis e não houve passe imediatamente anterior, **QUANDO** ele passa, **ENTÃO** a dupla adversária recebe 20 pontos de passe e a vez muda; se a sequência se tornar passe geral, esses 20 são substituídos pelos 50
2. **DADO** que é o início do jogo e o jogador não tem 6-6 nem pedras para começar, **QUANDO** ele passa, **ENTÃO** a dupla adversária marca 20 pontos
3. **DADO** que os outros três jogadores passam após a última jogada e seu autor pode jogar novamente, **QUANDO** ocorre galo (passe geral), **ENTÃO** a sequência vale somente 50 pontos para a dupla da última jogada e a vez retorna ao jogador que jogou, mantendo a raia em andamento
4. **DADO** que o jogador anterior passou, **QUANDO** o segundo jogador também passa consecutivamente, **ENTÃO** esse segundo passe não concede pontos, mas avança a vez e integra a sequência de passes.
5. **DADO** que o jogador tem pedras jogáveis, **QUANDO** ele tenta passar, **ENTÃO** o sistema rejeita o passe e anuncia vitória da dupla adversária

---

### User Story 4 - Bater e esvaziar a mão (Priority: P1)

Como jogador, quero poder vencer a raia jogando todas as minhas pedras até esvaziar a mão, para ganhar pontos da dupla adversária.

**Why this priority**: A batida é o objetivo principal de cada raia e determina a pontuação final da rodada.

**Independent Test**: Pode ser testado simulando um jogador que consegue jogar todas as 7 pedras até não ter mais nenhuma

**Acceptance Scenarios**:

1. **DADO** que o jogador tem apenas 1 pedra na mão, **QUANDO** ele joga essa pedra, **ENTÃO** ele bate e a raia termina
2. **DADO** que o jogador bate sem carroça final, **QUANDO** a raia termina, **ENTÃO** a dupla que bateu recebe a soma das pedras restantes dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo
3. **DADO** que o jogador bate com uma carroça (doble) como última pedra, **QUANDO** ocorre a batida, **ENTÃO** sua dupla recebe 20 pontos mais eventual pontuação das pontas da última jogada, sem contagem das mãos adversárias

---

### User Story 5 - Encerrar partida ao atingir 200 pontos (Priority: P2)

Como jogador, quero que o sistema verifique automaticamente quando uma dupla atinge 200 pontos ou mais ao final de uma raia, para determinar o vencedor da partida.

**Why this priority**: A condição de vitória define quando a partida termina, mas só é verificada após o fim de cada raia, tornando-a menos frequente que as ações anteriores.

**Independent Test**: Pode ser testado simulando múltiplas raias até que uma dupla atinja 200+ pontos

**Acceptance Scenarios**:

1. **DADO** que uma dupla tem 180 pontos e termina uma raia batendo, **QUANDO** são somados os pontos da raia resultando em 210, **ENTÃO** a dupla vence a partida e o jogo encerra
2. **DADO** que uma dupla atinge 205 pontos mas a raia ainda não terminou, **QUANDO** a raia continua, **ENTÃO** o jogo só verifica a vitória por pontuação após batida ou jogo fechado, contabilizando a pontuação final da raia
3. **DADO** que nenhuma dupla atingiu 200 pontos, **QUANDO** uma raia termina, **ENTÃO** o jogo continua para a próxima raia

---

### User Story 6 - Jogo fechado (tranca) com menos pontos na mão (Priority: P3)

Como jogador, quero que o sistema determine o vencedor de uma raia travada quem tem menos pontos nas pedras restantes, para lidar com situações de jogo fechado.

**Why this priority**: O cenário de tranca é menos comum que a batida normal, mas necessário para completar as regras do jogo.

**Independent Test**: Pode ser testado simulando uma situação onde nenhum jogador consegue jogar e todos passaram

**Acceptance Scenarios**:

1. **DADO** que o jogo está travado e ninguém pode mais jogar, **QUANDO** todos passaram, **ENTÃO** ganha quem tem menos pontos na mão
2. **DADO** que há empate de pontos na mão de tranca, **QUANDO** ocorre o empate, **ENTÃO** nenhuma dupla pontua pela tranca e o placar acumulado é preservado, independentemente de quem jogou por último
3. **DADO** que a raia terminou em tranca, **QUANDO** contam-se os pontos, **ENTÃO** a dupla com menos pontos recebe a soma das mãos da dupla adversária, arredondada para baixo ao múltiplo de 5 mais próximo

---

## Clarifications

### Decisões adicionais confirmadas em 2026-09-30

- O jogador entra escolhendo um apelido, sem cadastro, login ou senha. No multiplayer, pode criar uma sala ou informar o código de uma sala existente.

- Durante a partida, se um jogador humano perder a conexão, um jogador controlado pelo computador assume seu lugar, preservando mão, dupla e estado da partida. Cada jogada tem limite de 20 segundos. Ao esgotar os 20 segundos, o computador executa uma jogada válida pelo jogador naquele turno. Se não houver jogada válida, executa o passe conforme as regras do jogo. Para um humano ainda conectado, essa ação automática não transfere permanentemente o controle ao computador. Após reconectar, o humano retoma sua mesma posição no início do próximo turno que lhe couber, preservando mão, dupla e estado atual. A reconexão não desfaz jogadas já realizadas pelo computador nem interrompe o turno em andamento.

- O multiplayer começa pela criação de uma sala. A sala reúne quatro jogadores humanos, cada um no navegador de seu computador, para uma partida em duas duplas. Ao criar a sala, o sistema gera e exibe um código. Os demais jogadores entram informando esse código na interface web. No multiplayer, os próprios jogadores escolhem suas duplas na sala antes do início da partida. Cada dupla deve ter exatamente dois jogadores; a partida só pode começar com as duas duplas completas. As duplas permanecem fixas durante a partida. Quando os quatro jogadores estiverem na sala e houver exatamente dois em cada dupla, o sistema embaralha e distribui automaticamente as 28 pedras, sete por jogador, sem comando do criador da sala. Aplicam-se as regras de cinco, seis e sete carroças antes da primeira jogada; na primeira raia, quem receber o 6-6 inicia jogando essa pedra.

- Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.
- Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

- A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega. A mesa e as pedras terão estilo mesa de bar. O fluxo de jogo será operado por controles visuais; uma CLI de jogo não faz parte da entrega inicial. A interface web e sua integração com o motor ainda precisam ser implementadas.

- As duas pontas laterais saem da carroça inicial. Só ficam disponíveis após jogar pelo menos uma pedra em cada uma das duas pontas principais; a carroça inicial não conta como preenchimento desses ramos. Jogar várias pedras apenas em uma ponta principal não libera as laterais. A primeira pedra de cada lateral deve combinar com o naipe da carroça inicial.

- Se, após batida ou jogo fechado e a contabilização final da raia, os placares acumulados das duas duplas forem iguais e de 200 pontos ou mais, jogar outra raia, preservando o placar. Repetir enquanto houver empate ao fim da raia; não encerrar no primeiro desempate durante a raia. A abertura segue a regra do encerramento anterior: após batida, o batido; após tranca, quem receber o 6-6.

- Atingir ou ultrapassar 200 pontos durante a raia não encerra a partida. A vitória por pontuação só é verificada após a raia terminar por batida ou jogo fechado (tranca), com a pontuação final da raia contabilizada. Permanece a exceção já confirmada de vitória automática por 7 carroças.

- “Lá e Lô” não faz parte das regras deste projeto. O cenário e o bônus anteriormente mencionados foram removidos por esclarecimento do responsável.

- Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez.

- Se os quatro jogadores passam, é jogo fechado (tranca), não galo: a raia termina e não há bônus de 50 pontos de passe geral. O galo exige que o autor da última jogada possa jogar novamente após os passes dos outros três.

- Com exatamente 6 carroças na mão inicial, o jogador joga normalmente. Com 7 carroças na mão inicial de um jogador, sua dupla vence a partida automaticamente. A opção de recusa e o bônus de 50 pontos aplicam-se somente a exatamente 5 carroças.

- Se as somas das mãos das duas duplas forem iguais na tranca, nenhuma dupla recebe pontos por essa tranca, independentemente de quem jogou por último. Comparar as somas antes de qualquer arredondamento e preservar o placar já acumulado.

- Na tranca e na batida normal (sem carroça final), a dupla vencedora recebe a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo: `pontos = (soma_adversária // 5) * 5`. Somar as duas mãos antes de arredondar; não incluir a mão do parceiro nem subtrair a soma da dupla vencedora.

- Existe apenas um modo, com 4 jogadores em 2 duplas.
- Com 5 carroças na mão inicial, o jogador pode aceitar ou recusar jogar. Ao aceitar, sua dupla ganha 50 pontos no início. Se recusar, todos devolvem as 28 pedras, que são embaralhadas e distribuídas novamente (7 por jogador), sem conceder o bônus de 50 pontos.
- O passe vale 20 pontos para a dupla adversária; o segundo passe consecutivo não pontua. Quando os outros três jogadores passam após uma jogada e seu autor tem jogada disponível, ocorre galo (passe geral): a sequência vale somente 50 pontos para a dupla da última jogada, sem acumular os 20 pontos de passe. A raia continua e a vez retorna ao jogador que fez a última jogada.
- Depois de tranca, se houver próxima raia, quem receber a carroça de sena (6-6) inicia com essa pedra. Essa regra substitui a abertura pelo batido nesse caso.

### Session 2026-09-30

- Q: Como funciona o sistema de "4 pontas" para pontuação? → A: Pontuação sempre soma 4 pontas; não preenchidas valem 0. Início: carroça única (soma = soma dos dois lados da carroça, ex: 6-6 = 12). 2ª pedra: soma = carroça + ponta jogada. 3ª/4ª pedras (laterais): soma = pontas opostas + laterais (0 se vazias). 5ª+: soma completa das 4 pontas. As laterais saem da carroça inicial e só são liberadas depois de uma pedra jogada em cada ponta principal, além da própria carroça. Só marca pontos se a soma for múltiplo de 5.
- Q: A aplicação é para quantos jogadores? → A: 4 jogadores divididos em 2 duplas, conforme regras oficiais do dominó amazonense.
- Q: Qual é o valor do dobro 0 (bola/ovo) para pontuação? → A: Valor 0, não tem valor especial - é uma carroça como qualquer outra.
- Q: Como funciona a resolução de tranca e empates? → A: Maior soma de pontos na mão perde. A soma das mãos da dupla perdedora é concedida como pontos à dupla vencedora. Se os placares acumulados forem iguais e de 200+ pontos ao final da raia, seja por batida ou tranca, joga-se mais uma raia. Persistindo empate de placar ao final das raias seguintes, novas raias são jogadas. A soma das mãos da dupla perdedora é arredondada para baixo ao múltiplo de 5 mais próximo. Em caso de igualdade das somas das mãos, nenhuma dupla pontua pela tranca; a continuação da partida depende do placar acumulado.
- Q: Quem começa a primeira raia quando ninguém tem 6-6? → A: Isso não acontece - o 6-6 sempre será distribuído aleatoriamente entre os 4 jogadores no início, e quem recebe o 6-6 começa.
- Q: Como funciona quem inicia cada raia? → A: Primeira raia: quem tem o 6-6 inicia. Após batida: quem bateu na raia anterior inicia a próxima. Após tranca: quem receber o 6-6 inicia com ele. Se o batido não tiver carroça para iniciar (passou na raia anterior), a vez é para o próximo jogador na sequência.

---

## Edge Cases

- O que acontece quando um jogador inicia com 5 carroças? → Pode aceitar ou recusar jogar. Se aceitar, sua dupla ganha 50 pontos no início. Se recusar, todos devolvem as 28 pedras, que são embaralhadas e distribuídas novamente (7 por jogador), sem conceder o bônus de 50 pontos.
- O que acontece quando um jogador inicia com 6 carroças? → Joga normalmente, sem bônus de cinco carroças nem opção de recusa por essa regra.
- O que acontece quando um jogador inicia com 7 carroças? → Sua dupla vence a partida automaticamente.
- Como é determinado quem começa em raias posteriores? → Após batida, quem bateu inicia; se não tiver carroça para iniciar, vez passa para o próximo. Após tranca, quem receber o 6-6 inicia com ele
- Como funciona o dobro 0 (bola/ovo)? → Valor 0, sem valor especial - trata-se como carroça normal
- Como funciona a resolução de tranca e empates? → Maior soma de pontos na mão perde. A soma das mãos da dupla perdedora é concedida como pontos à dupla vencedora. Se os placares acumulados forem iguais e de 200+ pontos ao final da raia, seja por batida ou tranca, joga-se mais uma raia. Persistindo empate de placar ao final das raias seguintes, novas raias são jogadas. A soma das mãos da dupla perdedora é arredondada para baixo ao múltiplo de 5 mais próximo. Em caso de igualdade das somas das mãos, nenhuma dupla pontua pela tranca.
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
- **FR-005**: System MUST permitir as duas laterais ancoradas na carroça inicial somente após ao menos uma pedra jogada em cada ponta principal; não contar a carroça como preenchimento dos ramos; a primeira pedra lateral deve combinar com o naipe da carroça inicial
- **FR-005**: System MUST permitir passe quando jogador não tem pedras jogáveis
- **FR-006**: System MUST marcar 20 pontos para a dupla adversária por passe comum, não pontuar o segundo passe consecutivo e substituir a pontuação de passes da sequência por somente 50 pontos se ocorrer passe geral
- **FR-007**: System MUST detectar galo (passe geral) quando os outros três jogadores passam consecutivamente após uma jogada válida e seu autor tem jogada disponível; se ele também não puder jogar, tratar como jogo fechado, sem conceder os 50 pontos de galo
- **FR-008**: System MUST atribuir somente 50 pontos à dupla da última jogada no passe geral, sem acumular os pontos de passe da mesma sequência; manter a raia em andamento e devolver a vez ao autor da última jogada
- **FR-008.1**: System MUST reiniciar a sequência de passes após uma jogada válida e impedir pontuação duplicada do mesmo passe geral
- **FR-009**: System MUST detectar batida quando jogador joga sua última pedra
- **FR-010**: System MUST conceder à dupla que bateu sem carroça final a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondando o total para baixo ao múltiplo de 5 mais próximo
- **FR-010.5**: System MUST, na batida com carroça como última pedra, conceder à dupla 20 pontos mais eventual pontuação das pontas dessa jogada, sem contar as mãos adversárias e sem duplicar o crédito das pontas
- **FR-011**: System MUST verificar vitória por pontuação somente após batida ou jogo fechado, com a pontuação final da raia contabilizada; atingir 200+ durante a raia não deve encerrá-la. Preservar a vitória automática por 7 carroças de FR-017
- **FR-012**: System MUST resolver tranca comparando soma conjunta de pontos nas mãos de cada dupla (maior soma perde)
- **FR-013**: System MUST conceder à dupla vencedora da tranca a soma dos valores das pedras restantes nas mãos da dupla perdedora, arredondando o total para baixo ao múltiplo de 5 mais próximo; não usar a diferença entre as mãos
- **FR-013.1**: System MUST comparar as somas das mãos das duplas antes do arredondamento; em caso de igualdade na tranca, não declarar dupla vencedora da raia nem conceder pontos pela tranca, preservando o placar acumulado e ignorando quem jogou por último
- **FR-014**: System MUST determinar início da partida com jogador que recebe o 6-6 na distribuição aleatória das 28 pedras
- **FR-015**: System MUST determinar início da raia posterior a uma batida com quem bateu na rodada anterior. Se o batido não tiver carroça para iniciar, a vez passa para o próximo jogador na sequência.
- **FR-015.1**: System MUST iniciar a próxima raia após tranca com o jogador que receber a carroça de sena (6-6), exigindo essa pedra na abertura
- **FR-016**: System MUST permitir ao jogador com exatamente 5 carroças na mão inicial aceitar ou recusar jogar; conceder 50 pontos à sua dupla no início apenas se ele aceitar
- **FR-016.1**: System MUST, em caso de recusa do jogador com 5 carroças, recolher as 28 pedras de todos os jogadores, embaralhar e distribuir novamente 7 pedras para cada jogador, sem conceder o bônus de 50 pontos nem alterar o placar acumulado
- **FR-017**: System MUST declarar vitória automática da dupla quando um de seus jogadores receber 7 carroças na mão inicial, encerrando a partida independentemente do placar
- **FR-017.1**: System MUST prosseguir normalmente quando um jogador receber exatamente 6 carroças, sem conceder vitória automática, bônus de cinco carroças ou recusa por essa regra
- **FR-018**: System MUST jogar raia extra se os placares acumulados das duplas forem iguais e de 200+ pontos após batida ou tranca e contabilização final da raia, preservando o placar
- **FR-019**: System MUST continuar raias extras enquanto persistir empate dos placares acumulados de 200+ pontos ao final de cada raia; não encerrar por desempate durante a raia; aplicar as regras de abertura após batida ou tranca
- **FR-020**: System MUST distribuir 28 pedras aleatoriamente entre 4 jogadores (7 pedras cada) no início

- **FR-021**: System MUST oferecer partida solo com um humano e três jogadores controlados pelo computador, mantendo duas duplas e as mesmas regras
- **FR-022**: System MUST permitir uma partida entre quatro pessoas, cada uma em seu dispositivo, sincronizando mesa, turnos e placar
- **FR-023**: System MUST limitar a visão de cada participante à própria mão e às informações públicas; impedir acesso às mãos dos demais, inclusive do parceiro

- **FR-024**: System MUST disponibilizar os modos solo e multiplayer em interface web para navegador no computador, sem exigir instalação de cliente desktop

- **FR-025**: System MUST permitir criar uma sala multiplayer para reunir quatro jogadores humanos e iniciar uma partida em duas duplas; gerar e exibir um código da sala e permitir que os demais jogadores entrem informando esse código

- **FR-026**: System MUST permitir que os jogadores escolham suas duplas na sala antes da partida, limitando cada dupla a dois participantes e exigindo duas duplas completas para iniciar; manter a formação fixa durante a partida

- **FR-027**: System MUST substituir por participante controlado pelo computador o humano que perder a conexão durante a partida, preservando suas pedras, dupla e estado do jogo
- **FR-028**: System MUST limitar cada jogada a 20 segundos e exibir o tempo restante na interface; ao esgotar o tempo, executar automaticamente uma jogada válida naquele turno ou, se não houver nenhuma, o passe conforme as regras; manter o controle humano nos próximos turnos se ainda conectado

- **FR-029**: System MUST devolver ao humano reconectado o controle da sua mesma posição no próximo turno que lhe couber, mantendo mão, dupla e estado atual, sem desfazer jogadas do computador ou interromper o turno em andamento

- **FR-030**: System MUST permitir entrada com apelido, sem cadastro, login ou senha; manter identidade de sessão independente do apelido para a reconexão do participante original

- **FR-031**: System MUST embaralhar e distribuir automaticamente as 28 pedras quando a sala reunir quatro jogadores e duas duplas de dois, sem exigir comando do criador; aplicar as regras de carroças iniciais e atribuir a primeira jogada da primeira raia ao portador do 6-6

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

## Cenários de aceitação das decisões confirmadas

1. **DADO** um jogador com 5 carroças iniciais, **QUANDO** ele aceita jogar, **ENTÃO** sua dupla recebe 50 pontos no início, uma única vez.
2. **DADO** um jogador com 5 carroças iniciais, **QUANDO** ainda não respondeu, **ENTÃO** o bônus não é concedido automaticamente e a decisão de aceitar ou recusar permanece disponível.
3. **DADO** que a última pedra foi jogada pela dupla A, **QUANDO** ocorre galo, **ENTÃO** a sequência concede somente 50 pontos à dupla A, substituindo os pontos de passe da mesma sequência, e o autor da última jogada joga novamente sem encerrar a raia.
4. **DADO** que a raia terminou em tranca e a partida continua, **QUANDO** as pedras da próxima raia são distribuídas, **ENTÃO** o portador do 6-6 inicia jogando essa pedra, independentemente do batido de uma raia anterior.

5. **DADO** um jogador com 5 carroças iniciais, **QUANDO** ele recusa jogar, **ENTÃO** as 28 pedras são recolhidas, embaralhadas e distribuídas novamente, com 7 pedras por jogador, sem duplicatas, sem conceder os 50 pontos e preservando o placar acumulado. A decisão anterior não se aplica à nova distribuição.

6. **DADO** uma tranca com totais de mão de 20 e 37, **QUANDO** a dupla com 20 vence, **ENTÃO** recebe 35 pontos (37 arredondado), sem subtrair os 20.
7. **DADO** uma batida normal sem carroça final em que as mãos adversárias somam 18 e 19, **QUANDO** se calcula a contagem final, **ENTÃO** a dupla que bateu recebe 35 pontos pela contagem (18 + 19 = 37), excluindo a mão do parceiro.
8. **DADO** um total adversário de 0, 4, 5, 35, 37 ou 40, **QUANDO** se calcula a contagem na batida normal ou tranca, **ENTÃO** os pontos são respectivamente 0, 0, 5, 35, 35 e 40. Múltiplos exatos permanecem inalterados.

9. **DADO** que as duas duplas têm a mesma soma nas mãos ao trancar, **QUANDO** a tranca é resolvida, **ENTÃO** ambas recebem 0 pontos pela tranca, não há dupla vencedora da raia e o placar acumulado permanece inalterado, independentemente do autor da última jogada.
10. **DADO** que as mãos somam 31 e 34, **QUANDO** a tranca é resolvida, **ENTÃO** não há empate: a dupla com 31 vence e recebe 30 pontos pela soma adversária arredondada.

11. **DADO** um jogador com exatamente 6 carroças na distribuição, **QUANDO** se avalia a mão inicial, **ENTÃO** a partida segue normalmente, sem vitória automática, bônus de cinco carroças ou opção de recusa por essa regra.
12. **DADO** um jogador com as 7 carroças na distribuição, **QUANDO** se avalia a mão inicial, **ENTÃO** sua dupla vence a partida automaticamente, independentemente do placar, sem exigir uma jogada.

13. **DADO** que os outros três jogadores passaram e o autor da última jogada também não tem jogada disponível, **QUANDO** os quatro passam, **ENTÃO** ocorre jogo fechado (tranca), a raia termina e não se concede bônus de 50 pontos de galo. Aplicam-se a contagem das mãos e a regra de empate da tranca.

14. **DADO** que um jogador bate com carroça e a soma das pontas após a jogada vale 10 pontos, **QUANDO** a batida é pontuada, **ENTÃO** sua dupla recebe 30 pontos no total por essa jogada (20 + 10), independentemente das mãos adversárias.
15. **DADO** que um jogador bate com carroça e a soma das pontas não pontua, **QUANDO** a batida é pontuada, **ENTÃO** sua dupla recebe somente 20 pontos por essa jogada, sem contagem das mãos adversárias.

16. **DADO** que uma dupla alcança ou ultrapassa 200 pontos com a raia em andamento, **QUANDO** a pontuação é atualizada, **ENTÃO** a raia continua; a vitória por pontuação só é verificada após batida ou tranca e a contabilização final da raia.

17. **DADO** que o placar acumulado fica em 200–200 ou 215–215 após batida ou tranca e contagem final, **QUANDO** a vitória é verificada, **ENTÃO** a partida continua em outra raia com o placar preservado. Se o empate persistir ao final dessa raia, joga-se outra.
18. **DADO** uma raia extra por empate acima da meta, **QUANDO** uma dupla assume a liderança durante a raia, **ENTÃO** a raia continua até batida ou jogo fechado antes de verificar vitória por pontuação.

19. **DADO** uma carroça inicial 6-6, **QUANDO** se joga 6-3 na esquerda e depois 3-2 também na esquerda, **ENTÃO** as laterais continuam bloqueadas.
20. **DADO** essa mesa, **QUANDO** se joga 6-4 na direita, **ENTÃO** as duas laterais ficam disponíveis, ambas ancoradas no naipe 6 da carroça inicial; 6-1 pode abrir uma lateral, mas 2-1 não pode.

21. **DADO** o aplicativo gráfico integrado ao motor, **QUANDO** o usuário inicia uma partida e seleciona uma pedra e uma ponta válida na tela, **ENTÃO** a jogada é executada e mesa, turno e placar são atualizados visualmente, sem exigir comandos de terminal.

22. **DADO** que o jogador escolhe jogar sozinho, **QUANDO** a partida começa, **ENTÃO** há um humano e três jogadores controlados pelo computador, distribuídos em duas duplas sob as mesmas regras.
23. **DADO** quatro pessoas conectadas em dispositivos distintos, **QUANDO** uma jogada válida é executada, **ENTÃO** todos recebem a atualização da mesa, do turno e do placar, sem receber as mãos privadas dos outros jogadores.

24. **DADO** que o usuário escolhe multiplayer, **QUANDO** solicita criar uma sala, **ENTÃO** uma sala é criada para reunir quatro jogadores humanos antes do início da partida.

25. **DADO** que uma sala foi criada, **QUANDO** o criador consulta a sala, **ENTÃO** vê o código que os demais jogadores podem informar para entrar.
26. **DADO** um código de sala existente com vaga, **QUANDO** outro jogador informa esse código, **ENTÃO** entra nessa sala; códigos inexistentes ou salas com quatro participantes são rejeitados com mensagem clara.

27. **DADO** que os quatro jogadores estão na sala, **QUANDO** escolhem suas duplas, **ENTÃO** o sistema respeita a escolha, impede um terceiro integrante na mesma dupla e só permite iniciar com dois jogadores em cada dupla.

28. **DADO** um humano participando da partida, **QUANDO** sua conexão é perdida, **ENTÃO** um jogador de computador assume a mesma posição, mão e dupla, sem redistribuir as pedras ou reiniciar a partida.
29. **DADO** o início de uma vez de jogar, **QUANDO** o turno é disponibilizado, **ENTÃO** o limite é de 20 segundos e a interface mostra o tempo restante.

30. **DADO** que um humano conectado deixa os 20 segundos expirarem com uma jogada disponível, **QUANDO** o prazo vence, **ENTÃO** o computador executa uma jogada válida por ele somente naquele turno; o humano mantém controle nos turnos seguintes.
31. **DADO** que o prazo vence sem jogada válida disponível, **QUANDO** a ação automática é executada, **ENTÃO** ocorre passe conforme as regras, sem tentar encaixe inválido.
32. **DADO** uma ação humana recebida simultaneamente ao vencimento do prazo, **QUANDO** o servidor resolve o turno, **ENTÃO** apenas uma ação válida é aplicada, sem duplicar pedras ou pontuação.

33. **DADO** que um humano desconectado foi substituído por computador, **QUANDO** ele reconecta, **ENTÃO** retoma o controle no próximo turno que lhe couber, recebe sua mão atual e mantém a mesma dupla, sem desfazer jogadas já executadas.
34. **DADO** que houve reconexão durante um turno em andamento, **QUANDO** a retomada é preparada, **ENTÃO** o turno atual não é reiniciado nem recebe ações simultâneas do computador e do humano; a troca ocorre no próximo turno desse jogador.

35. **DADO** que o usuário acessa o aplicativo, **QUANDO** informa seu apelido, **ENTÃO** pode escolher solo, criar uma sala ou entrar por código sem cadastrar conta ou fornecer senha.
36. **DADO** um participante desconectado, **QUANDO** outro visitante usa o mesmo apelido, **ENTÃO** o apelido sozinho não permite assumir a posição ou acessar a mão do participante original; a retomada depende da sessão original.

37. **DADO** uma sala aguardando participantes e formação das duplas, **QUANDO** passa a reunir quatro jogadores com dois em cada dupla, **ENTÃO** o sistema inicia uma única distribuição automática de sete pedras por jogador, sem ação especial do criador da sala.
38. **DADO** essa distribuição inicial, **QUANDO** as decisões de carroças iniciais são resolvidas e a partida continua, **ENTÃO** quem recebeu o 6-6 faz a primeira jogada com essa pedra, independentemente de quem criou a sala.

## Pendências relacionadas

- Tecnologia do frontend web, hospedagem e alcance do multiplayer (internet, rede local ou ambos).
- Nível de dificuldade dos jogadores controlados pelo computador.

- As demais divergências levantadas na revisão continuam pendentes quando não resolvidas explicitamente pelas decisões acima.

## Assumptions

- Usuários têm familiaridade básica com regras de dominó
- A aplicação será implementada primeiro em Python conforme constituição do projeto
- A entrega inicial inclui interface gráfica com mesa e pedras; regras de negócio permanecem independentes da GUI. Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.
- Jogadores individuais são agrupados em duplas fixas durante toda a partida
- O conjunto de pedras é o duplo-6 (28 pedras totais)
- O jogo evolui no sentido anti-horário (tradicional no Amazonas)
