# Revisão do projeto — 30/09/2026

## Atualização após esclarecimentos do responsável

As constatações abaixo registram a revisão original. Em seguida, foram confirmadas e incorporadas à documentação estas decisões:

- Um único modo: 4 jogadores em 2 duplas. Simplex retirado do escopo; suas lacunas não são mais pendências do produto.
- Cinco carroças iniciais: o jogador pode aceitar ou recusar jogar; se aceitar, sua dupla ganha 50 pontos no início. Se recusar, todos devolvem as 28 pedras, que são embaralhadas e distribuídas novamente (7 por jogador), sem conceder o bônus de 50 pontos.
- O passe vale 20 pontos para a dupla adversária; o segundo passe consecutivo não pontua. Quando os outros três jogadores passam após uma jogada e seu autor tem jogada disponível, ocorre galo (passe geral): a sequência vale somente 50 pontos para a dupla da última jogada, sem acumular os 20 pontos de passe. A raia continua e a vez retorna ao jogador que fez a última jogada. Se os quatro jogadores passam, é jogo fechado (tranca), não galo: a raia termina e não há bônus de 50 pontos de passe geral. O galo exige que o autor da última jogada possa jogar novamente após os passes dos outros três. A distinção e o não acúmulo de galo com tranca estão resolvidos.
- Após tranca: quem receber a carroça de sena (6-6) inicia a próxima raia com ela.
- Na tranca e na batida normal (sem carroça final), a dupla vencedora recebe a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo: `pontos = (soma_adversária // 5) * 5`. Somar as duas mãos antes de arredondar; não incluir a mão do parceiro nem subtrair a soma da dupla vencedora. Isso resolve o item 6 e o arredondamento da batida no item 9; a exceção da carroça final foi definida posteriormente: Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez. A referência a “Lá e Lô” era indevida: o responsável confirmou que essa regra não existe no jogo. Cenário e bônus retirados da especificação e do backlog; não há pendência sobre esse tema.
- Se as somas das mãos das duas duplas forem iguais na tranca, nenhuma dupla recebe pontos por essa tranca, independentemente de quem jogou por último. Comparar as somas antes de qualquer arredondamento e preservar o placar já acumulado. Isso resolve o item 5; empate de placar da partida é uma questão separada.

Isso resolve o item 1, a regra de cinco carroças do item 2, a distinção entre galo e encerramento do item 3 e o destinatário e não acúmulo com passes do item 4 e a abertura após bloqueio do item 7. O item 12 foi retirado do escopo. Os bugs de implementação permanecem.

- Com exatamente 6 carroças na mão inicial, o jogador joga normalmente. Com 7 carroças na mão inicial de um jogador, sua dupla vence a partida automaticamente. A opção de recusa e o bônus de 50 pontos aplicam-se somente a exatamente 5 carroças. Isso resolve a pendência de vitória por carroças iniciais do item 2.

- Atingir ou ultrapassar 200 pontos durante a raia não encerra a partida. A vitória por pontuação só é verificada após a raia terminar por batida ou jogo fechado (tranca), com a pontuação final da raia contabilizada. Permanece a exceção já confirmada de vitória automática por 7 carroças. Isso resolve o momento de verificação do item 8; o empate de placar também foi confirmado: Se, após batida ou jogo fechado e a contabilização final da raia, os placares acumulados das duas duplas forem iguais e de 200 pontos ou mais, jogar outra raia, preservando o placar. Repetir enquanto houver empate ao fim da raia; não encerrar no primeiro desempate durante a raia. A abertura segue a regra do encerramento anterior: após batida, o batido; após tranca, quem receber o 6-6.

- As duas pontas laterais saem da carroça inicial. Só ficam disponíveis após jogar pelo menos uma pedra em cada uma das duas pontas principais; a carroça inicial não conta como preenchimento desses ramos. Jogar várias pedras apenas em uma ponta principal não libera as laterais. A primeira pedra de cada lateral deve combinar com o naipe da carroça inicial. Isso resolve a origem e o gatilho de abertura das laterais do item 11. A implementação permanece pendente.

- A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega. A mesa e as pedras terão estilo mesa de bar. O fluxo de jogo será operado por controles visuais; uma CLI de jogo não faz parte da entrega inicial. A interface web e sua integração com o motor ainda precisam ser implementadas. A escolha de interface está resolvida; Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista. Plataforma confirmada: navegador no computador; framework web e alcance da rede ainda pendentes.

- O multiplayer começa pela criação de uma sala. A sala reúne quatro jogadores humanos, cada um no navegador de seu computador, para uma partida em duas duplas. Ao criar a sala, o sistema gera e exibe um código. Os demais jogadores entram informando esse código na interface web. No multiplayer, os próprios jogadores escolhem suas duplas na sala antes do início da partida. Cada dupla deve ter exatamente dois jogadores; a partida só pode começar com as duas duplas completas. As duplas permanecem fixas durante a partida. Quando os quatro jogadores estiverem na sala e houver exatamente dois em cada dupla, o sistema embaralha e distribui automaticamente as 28 pedras, sete por jogador, sem comando do criador da sala. Aplicam-se as regras de cinco, seis e sete carroças antes da primeira jogada; na primeira raia, quem receber o 6-6 inicia jogando essa pedra. Criação de sala e entrada por código estão confirmadas.

- Durante a partida, se um jogador humano perder a conexão, um jogador controlado pelo computador assume seu lugar, preservando mão, dupla e estado da partida. Cada jogada tem limite de 20 segundos. Ao esgotar os 20 segundos, o computador executa uma jogada válida pelo jogador naquele turno. Se não houver jogada válida, executa o passe conforme as regras do jogo. Para um humano ainda conectado, essa ação automática não transfere permanentemente o controle ao computador. Após reconectar, o humano retoma sua mesma posição no início do próximo turno que lhe couber, preservando mão, dupla e estado atual. A reconexão não desfaz jogadas já realizadas pelo computador nem interrompe o turno em andamento.

- O jogador entra escolhendo um apelido, sem cadastro, login ou senha. No multiplayer, pode criar uma sala ou informar o código de uma sala existente.

## Parecer

A proposta faz sentido e separar o domínio da interface é uma boa direção. O estado atual é um protótipo incompleto: existem regras incompatíveis entre documentos, dois escopos sem relação definida e falhas que impedem a progressão da mesa. Antes de ampliar a interface, é necessário consolidar as regras e entregar uma partida completa no domínio.

Revisão baseada no código de produção, testes, README, configuração, PDF local, constituição, especificações 001/002, modelo de dados, planejamento, pesquisa e quickstart. As regras do PDF são tratadas como referência local, sem afirmar que representam todas as variantes regionais. Não foram alteradas regras nem código de produção.

## Falhas de implementação

| Prioridade | Evidência | Impacto e ação necessária |
|---|---|---|
| P0 | `src/domino/domain/board.py:38-47,140-147,218-221` | `free_side_value` mistura valor de encaixe e contribuição à pontuação. Após abrir com 6–6, ambas as pontas exigem 12: nenhuma das 28 peças pode jogar. Separar esses conceitos. |
| P1 | `src/domino/domain/board.py:153-165` | `opposite_value` é calculado e descartado. Ao encaixar o lado B de 4–3 numa ponta 3, a nova ponta permanece 3 em vez de 4. A abertura não dupla também usa B nas duas extremidades. Guardar orientação/lado livre real. |
| P1 | `src/domino/domain/board.py:128-138,239-243` | As laterais são liberadas com base em posições que já receberam a peça inicial; depois continuam `None` e rejeitam a primeira conexão. Definir âncora de cada ramo e condição precisa de abertura. |
| P1 | `src/domino/domain/scorer.py:52-82` | Pontuação usa soma/5 × multiplicador, mas FR-004 da especificação 001 manda atribuir a própria soma. Uma abertura 5–5 produz soma 20 e 8 pontos, enquanto a especificação prevê soma 10 e 10 pontos. Há dupla contagem da abertura e fórmula divergente. |
| P1 | `src/domino/domain/scorer.py:219-225,265-285` | Batida inclui todos exceto o vencedor, portanto inclui o parceiro em partidas de quatro jogadores. Bloqueio compara jogadores individualmente, sem conceder a soma das mãos adversárias arredondada para baixo ao múltiplo de 5, conforme esclarecimento posterior. Os calculadores não satisfazem o modo amazonense. |
| P1 | `src/domino/core.py`, árvore de `src/domino` | Não há implementação de jogadores, duplas, distribuição, turnos, raias, partida, passes, galo ou vitória acumulada. `core.py` apenas reexporta classes. Falta o fluxo que conecte os componentes e preserve as 28 peças sem duplicatas. |
| P1 | `pyproject.toml:43-48`; `src/domino/gui/main.py:7,22-23` | Empacotamento e entry point usam `src.domino`, mas a GUI importa `domino`. O ajuste manual aponta para `src/src`. Uniformizar namespace e verificar instalação limpa e execução fora do repositório. |
| P1 | `src/domino/gui/main.py:174-240`; `README.md` | A interface cria uma mesa vazia e rótulos, sem ações para jogar ou passar. A CLI anunciada no README não existe. Documentar o estado como protótipo e escolher uma interface para o MVP. |
| P2 | `src/domino/gui/main.py:77-95,164-168` | O desenho das pintas ignora a coordenada Y calculada e não desloca corretamente o lado direito. A carroça central cria um widget local sem pai e sem exibição. Corrigir quando a interface entrar no escopo executável. |

## Definições e conflitos que precisam ser resolvidos

1. **Escopo vigente.** A constituição e a especificação 001 exigem quatro jogadores em duplas, quatro pontas e 200 pontos. A especificação 002 exige dois jogadores, duas pontas, bico sem compra e meta padrão 100. Declarar se 002 substitui 001, é etapa intermediária ou segundo modo. Se ambos existirem, separar políticas de regras e seus testes.
2. **Fonte normativa.** Definir a precedência entre PDF, constituição e esclarecimentos da especificação. O PDF, art. 11, permite solicitar rearme com cinco carroças; os documentos atribuem 50 pontos. Vitória automática com seis carroças consta da especificação, mas não do PDF. Uma variante deliberada precisa ser identificada como tal.
3. **Galo versus tranca.** Com passes obrigatórios, quatro passes seguidos implicam ausência de jogadas para todos. Detectar tranca imediatamente pode impedir galo de ocorrer. Especificar gatilho, momento do encerramento e prioridade de cada evento.
4. **Destinatário e acúmulo dos pontos do galo.** O PDF, art. 7, beneficia quem anuncia; a especificação menciona a dupla adversária e marcação automática. Definir adversária de quem e se os 50 acumulam com os quatro passes de 20 e com a contagem de tranca.
5. **Empate na tranca.** A história 6 e a constituição fazem perder quem jogou por último; os esclarecimentos posteriores da especificação 001 dizem que ninguém pontua. Consolidar uma regra. No Simplex, desempatar mãos iguais gera diferença zero: esclarecer o efeito prático do vencedor da rodada.
6. **Pontuação de tranca.** O PDF, art. 5, fala em converter a contagem da dupla com maior mão; a especificação define diferença das mãos. Registrar exemplos numéricos que fixem a interpretação, inclusive arredondamento.
7. **Próxima abertura depois de bloqueio.** “Quem bateu começa” não cobre rodadas sem batida. O PDF determina 6–6 após fechamento. Falta essa regra no fluxo especificado, especialmente no Simplex. Para abertura sem carroça no amazonense, explicitar destinatário dos 20 pontos e sequência de jogadores.
8. **Encerramento da partida e empate de placar.** A especificação 001 verifica vitória no fim da raia, enquanto o README sugere vitória imediata ao atingir 200. Definir comparação dos dois placares e empate após batida, além de empate na tranca. O art. 4 do PDF permite continuar a mão após 200.
9. **Batida e bônus.** Definir se a contagem das mãos na batida arredonda para múltiplos de cinco, se a última jogada acumula pontos de mesa, contagem e bônus de carroça. A revisão original encontrou uma referência indevida a “Lá e Lô”; posteriormente, o responsável confirmou sua exclusão. Esse ponto está resolvido.
10. **Infrações digitais.** Decidir quais ações inválidas são apenas rejeitadas e quais encerram a partida. PDF menciona punição por encaixe indevido, mas a história 1 apenas rejeita a jogada. Definir se anúncios, dicas e tempo de jogada fazem parte do aplicativo ou são regras presenciais fora do MVP.
11. **Topologia da mesa.** Definir de onde nascem as laterais, com que naipe encaixam, o que significa “duas pontas preenchidas”, se carroças posteriores criam ramos e como distinguir ponta vazia de ponta com valor zero. Exemplos precisam informar peça, lado de conexão e ponta alvo em cada passo.
12. **Simplex: carroças e início.** FR-008 transforma 6–6 em ponta 12, incompatível com o conjunto 0–6. Separar encaixe de eventual valor de contagem. Definir ordenação completa da “peça mais alta”, obrigação de jogar a peça selecionada e escolha do iniciador após bloqueio. FR-015 exige meta configurável, enquanto as premissas deixam isso para o futuro.
13. **Experiência de jogo.** Escolher CLI ou GUI para o primeiro produto jogável e definir interação local e privacidade das mãos. No Simplex, bots e rede estão fora do escopo; falta descrever como dois humanos alternam o uso do dispositivo.
14. **Contratos do motor.** Especificar validação de jogador da vez, propriedade da peça, unicidade independente da orientação, rejeição sem alteração parcial, proibição de ações após encerramento e aplicação única da pontuação. Não é necessário criar muitas camadas para garantir essas invariantes.

## Documentação e testes

- README apresenta como implementados CLI, arquitetura completa e cobertura superior a 80%, sem corresponder à árvore atual. O arquivo LICENSE referenciado não existe.
- README/research pedem Python 3.12; projeto/constituição permitem 3.11. Dependências documentadas também divergem das declaradas.
- A especificação 001 repete FR-005. O quickstart, linhas 235–239, afirma que soma 16 marca 15 pontos, contrariando o requisito de múltiplo de cinco.
- Testes incluem peças inválidas 3–7, duplicam pedras do conjunto e usam lado de conexão incompatível. Há expectativas que perpetuam erros do modelo. Corrigir as regras de referência antes de considerar a suíte um oráculo confiável.
- A exigência de distribuições diferentes em toda inicialização, na especificação 002, não é garantida por aleatoriedade. Testar conservação do conjunto, distribuição e reprodutibilidade com seed; evitar testes probabilísticos que falhem por coincidência válida.
- Não há pipeline de CI no repositório. Cobertura, lint e tipos devem representar resultados medidos, distinguindo metas de garantias existentes.

## Validação direta

Reproduções executadas com Python, sem dependências externas:

- 6–6 inicial → zero peças do conjunto completo têm movimento válido.
- 5–5 inicial → evento com soma 20, multiplicador 2 e 8 pontos.
- Lado 3 de 4–3 conectado à ponta 3 → ponta permanece 3.
- Após liberar laterais → primeira inserção lateral falha com `No piece at EndType.LATERAL_TOP to connect to`.

## Ordem recomendada

1. Declarar o escopo ativo e consolidar as decisões de regras acima em uma especificação única por modo.
2. Criar exemplos determinísticos de abertura, laterais, carroças, pontuação, passes e encerramento.
3. Corrigir mesa e calculadores, usando esses exemplos como testes de aceitação.
4. Implementar uma partida completa no domínio, incluindo distribuição, turnos e transição entre rodadas.
5. Conectar uma interface mínima; alinhar instalação, README e verificações automáticas ao que realmente funciona.

## Resultados das ferramentas

- **pytest 9.1.1, Python 3.12.4:** 72 testes coletados; 49 aprovados, 16 falhas e 7 erros de preparação. A execução inicial com Python 3.10 apresentou os mesmos resultados; a confirmação foi feita em 3.12, compatível com a documentação.
- **Cobertura com branches:** 75,89% no relatório produzido pela configuração atual; o gate de 80% falha. A GUI não aparece no denominador desse relatório, portanto esse número não representa cobertura de toda a aplicação.
- **Ruff 0.16.9:** 76 ocorrências em `src`, incluindo nomes indefinidos, imports e variáveis sem uso, além de estilo e documentação.
- **mypy 2.3.1:** 26 erros em 3 arquivos. Três são imports de PyQt6 ausente no ambiente isolado; os demais incluem anotações faltantes, `callable` usado como tipo, retornos `Any` e acesso opcional não validado. O total deve ser reavaliado após instalar todas as dependências da aplicação.
- Ferramentas instaladas em ambiente temporário em `/tmp`, sem alterar dependências do projeto. A confirmação em Python 3.12 reaproveitou os módulos Python desse ambiente; o coverage usou seu tracer Python, com aviso sobre ausência da extensão C compatível.
- GUI não executada visualmente; problemas de desenho e empacotamento foram identificados por leitura do código. Nenhuma alegação de validação visual ou instalação completa do aplicativo.
