# Constituição do Domino Amazonense

> Baseado nas Regras Oficiais do Dominó Amazonense praticadas em encontros e confrarias do Amazonas

## Glossário de Termos

- **Dominó**: Palavra dita ao fim de uma raia
- **Pedra**: Nome utilizado para denominar qualquer peça do jogo dominó
- **Branco**: Naipe com 0 pontos
- **Ás**: Naipe com 1 ponto
- **Duque**: Naipe com 2 pontos
- **Terno**: Naipe com 3 pontos
- **Quadra**: Naipe com 4 pontos
- **Quina**: Naipe com 5 pontos
- **Sena**: Naipe com 6 pontos
- **Passe**: Impossibilidade jogada pelo jogador da vez
- **Galo (passe geral)**: Os outros três jogadores passam após uma jogada e seu autor pode jogar novamente; vale somente 50 pontos para a dupla da última jogada e devolve a vez ao mesmo jogador, sem encerrar a raia
- **Gato**: Jogada indevida, ocasiona erro de contagem no jogo dominó
- **Raia**: Jogo onde a pontuação mínima entre duplas é de 200 pontos
- **Batida**: Ação onde o jogador da vez joga sua última pedra
- **Batido**: Jogador que jogou a última pedra do jogo anterior referente à raia atual
- **Saído**: Jogador que jogou a primeira pedra da raia
- **Carroça**: Pedra com dois lados equivalentes (doble)
- **Ficha**: Elemento que pode ser utilizado para marcação de pontos
- **Parceiro**: Qualquer um dos jogadores da dupla

## Princípios Fundamentais

### I. Desenvolvimento Primeiro em Python

O domínio e os serviços da aplicação permanecem em Python. A entrega será uma aplicação web acessada pelo navegador no computador; a tecnologia do frontend será definida no planejamento técnico.

- Usar Python 3.11+ com type hints obrigatórios
- Seguir PEP 8 e PEP 257 para estilo e documentação
- Utilizar virtual environments (venv ou poetry) para isolamento de dependências
- Bibliotecas devem ser autocontidas, testáveis independentemente e bem documentadas

### Plataforma

A plataforma de entrega é web para computador: o jogador acessa a interface gráfica pelo navegador, sem instalar um aplicativo desktop. Solo e multiplayer usam essa mesma interface. O protótipo PyQt6 existente não é a interface de entrega.

### II. Estilo Visual "Mesa de Bar"

A interface da aplicação deve capturar a autêntica atmosfera de uma mesa de bar amazonense:

- **Paleta de cores**: Madeira escura (marrom café, bordô), verde feltro, tons quentes de âmbar e dourado
- **Texturas**: Superfície de madeira rústica, detalhes em couro desgastado, iluminação ambiente suave
- **Atmosfera**: Acabamento premium com nostalgia, evocando confrarias e encontros informais
- **Elementos visuais**: Pedras de dominó realistas, fichas com brilho metálico, sombras suaves
- **Tipografia**: Fontes clássicas e legíveis, com peso médio a negrito para destaques
- **Iluminação**: Efeitos de luz ambiente, destaques estratégicos nas pedras e mesa

### III. Arquitetura Limpa

O código deve seguir os princípios de arquitetura limpa:

- Separação clara de responsabilidades em camadas (Domain, Application, Infrastructure, Presentation)
- Regras de negócio independentes de frameworks, bancos de dados e interfaces externas
- Injeção de dependência para desacoplar componentes
- Regra de dependência: camadas internas não conhecem as externas
- Entidades de negócio são o coração do sistema, imutáveis e independentes

### III. Testes Primeiros (NON-NEGOTIABLE)

TDD obrigatório em todo o projeto:

- Testes escritos → User approved → Tests fail → Então implementar
- Ciclo Red-Green-Refactor estritamente enforced
- Cobertura mínima de 80% para código de produção
- Testes unitários para lógica de negócio, testes de integração para camadas externas
- Tests devem rodar localmente e no CI antes de qualquer merge

### IV. Arquitetura Modular

A aplicação deve ser organizada em módulos independentes:

- Domínio de jogo separado da UI e infraestrutura
- Regras do dominó amazonense encapsuladas em módulo próprio
- Cada módulo deve ter responsabilidades bem definidas e únicas
- Interfaces claras entre módulos via contracts/interfaces
- Facilita testes, manutenção e extensão futura

### V. Documentação de Decisões

Todas as decisões arquiteturais devem ser documentadas:

- Usar ADRs (Architecture Decision Records) no formato padrão
- Documentar contexto, decisão consequentes e alternativas consideradas
- ADRs devem ser versionados junto com o código
- Revisar e atualizar ADRs quando o contexto mudar

## Regras do Jogo Domino Amazonense

### Configuração de Jogadores

Há duas formas de participação, com o mesmo conjunto de regras e sempre quatro jogadores em duas duplas: solo (um humano e três jogadores controlados pelo computador, incluindo seu parceiro) e multiplayer (quatro pessoas, cada uma em seu próprio dispositivo). Não há alternância de pessoas no mesmo computador como modalidade prevista.

Cada jogador vê apenas sua própria mão, a mesa e as informações públicas da partida. A mão do parceiro também é privada. Os jogadores controlados pelo computador devem decidir usando sua própria mão e as informações públicas, sem acesso às mãos alheias.

- Existe apenas um modo de jogo: dominó amazonense com 4 jogadores em 2 duplas. Simplex não faz parte do escopo.

- 4 jogadores divididos em 2 duplas (2 jogadores por dupla)
- Cada jogador recebe 7 pedras na distribuição inicial
- O conjunto usado é o duplo-6 (28 pedras totais)
- Partida disputada até 200 pontos ou superior

### Mesa e Laterais

As duas pontas laterais saem da carroça inicial. Só ficam disponíveis após jogar pelo menos uma pedra em cada uma das duas pontas principais; a carroça inicial não conta como preenchimento desses ramos. Jogar várias pedras apenas em uma ponta principal não libera as laterais. A primeira pedra de cada lateral deve combinar com o naipe da carroça inicial.

### Sistema de Pontuação

- Pontuação ocorre apenas quando as 4 pontas do jogo somam múltiplos de 5
- Quando a soma das 4 pontas é divisível por 5, a dupla que jogou marca pontos
- Pontuação : soma das 4 pontas  se a soam der múltiplo de 5 vale a quantidade somada
- Exemplo: se as pontas somam 10, marca 10 pontos; se somam 15, marca 15 pontos

### Dobres (Carroças)

- Dobres: 6-6, 5-5, 4-4, 3-3, 2-2, 1-1, 0-0
- Dobres funcionam como pedras especiais e devem ser colocados transversalmente
- Ao colocar um doble, o próximo jogador deve jogar no doble (em algumas variações)

### Movimentos Especiais e Pontuação

- Na batida com carroça, a dupla recebe 20 pontos mais a pontuação das pontas da última jogada, se houver (soma múltipla de 5). Não se somam as mãos adversárias nesse caso. A pontuação das pontas deve ser creditada uma única vez.

- Batida normal (esvaziar as pedras): a dupla que bateu ganha a soma das pedras restantes dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo
- Iniciar com 5 carroças: o jogador pode aceitar ou recusar jogar. Se aceitar, sua dupla recebe 50 pontos no início. Se recusar, todos devolvem as 28 pedras, que são embaralhadas e distribuídas novamente (7 por jogador), sem conceder o bônus de 50 pontos.
- Com exatamente 6 carroças na mão inicial, o jogador joga normalmente. Com 7 carroças na mão inicial de um jogador, sua dupla vence a partida automaticamente. A opção de recusa e o bônus de 50 pontos aplicam-se somente a exatamente 5 carroças.

### Tempo e Continuidade

Durante a partida, se um jogador humano perder a conexão, um jogador controlado pelo computador assume seu lugar, preservando mão, dupla e estado da partida. Cada jogada tem limite de 20 segundos. Ao esgotar os 20 segundos, o computador executa uma jogada válida pelo jogador naquele turno. Se não houver jogada válida, executa o passe conforme as regras do jogo. Para um humano ainda conectado, essa ação automática não transfere permanentemente o controle ao computador. Após reconectar, o humano retoma sua mesma posição no início do próximo turno que lhe couber, preservando mão, dupla e estado atual. A reconexão não desfaz jogadas já realizadas pelo computador nem interrompe o turno em andamento.

### Fluxo do Jogo

- Começa quem tem 6-6 (a carroça maior) ou sorteou a peça mais alta
- Jogo evolui no sentido anti-horário (tradicional no Amazonas)
- Objetivo: marcar pontos jogando pedras ou esvaziar a mão para bater
- Pedras devem combinar com as pontas disponíveis na mesa
- Se não tiver jogada disponível (inclusive no início do jogo), o jogador passa
- O passe vale 20 pontos para a dupla adversária; o segundo passe consecutivo não pontua. Quando os outros três jogadores passam após uma jogada e seu autor tem jogada disponível, ocorre galo (passe geral): a sequência vale somente 50 pontos para a dupla da última jogada, sem acumular os 20 pontos de passe. A raia continua e a vez retorna ao jogador que fez a última jogada.
- Após batida, quem bateu inicia a próxima raia. Após tranca, quem receber a carroça de sena (6-6) inicia a próxima raia com ela.

- Se os quatro jogadores passam, é jogo fechado (tranca), não galo: a raia termina e não há bônus de 50 pontos de passe geral. O galo exige que o autor da última jogada possa jogar novamente após os passes dos outros três.

### Condições de Vitória

- Se, após batida ou jogo fechado e a contabilização final da raia, os placares acumulados das duas duplas forem iguais e de 200 pontos ou mais, jogar outra raia, preservando o placar. Repetir enquanto houver empate ao fim da raia; não encerrar no primeiro desempate durante a raia. A abertura segue a regra do encerramento anterior: após batida, o batido; após tranca, quem receber o 6-6.

- Atingir ou ultrapassar 200 pontos durante a raia não encerra a partida. A vitória por pontuação só é verificada após a raia terminar por batida ou jogo fechado (tranca), com a pontuação final da raia contabilizada. Permanece a exceção já confirmada de vitória automática por 7 carroças.
- Uma raia termina quando alguém "bate" (esvazia todas as pedras da mão)
- Bater = não ter mais pedras em posse após jogar a última pedra
- Na tranca e na batida normal (sem carroça final), a dupla vencedora recebe a soma dos valores das pedras restantes nas mãos dos dois adversários, arredondada para baixo ao múltiplo de 5 mais próximo: `pontos = (soma_adversária // 5) * 5`. Somar as duas mãos antes de arredondar; não incluir a mão do parceiro nem subtrair a soma da dupla vencedora.
- Se ninguém bater e o jogo fechar (tranca), ganha quem tem menos pontos na mão
- Se as somas das mãos das duas duplas forem iguais na tranca, nenhuma dupla recebe pontos por essa tranca, independentemente de quem jogou por último. Comparar as somas antes de qualquer arredondamento e preservar o placar já acumulado.
- Pontuação é em conjunto com a dupla (pontua-se em conjunto, não individual)

## Restrições Adicionais

### Stack Tecnológico

- Python 3.11+ como linguagem principal
- pytest para framework de testes
- Black + ruff para formatação e linting
- mypy para type checking
- FastAPI ou similar para APIs (se aplicável)
- SQLite/PostgreSQL para persistência (se necessário)

### Padrões de Qualidade de Código

- Zero warnings em linters
- Type hints em todas as funções e classes
- Docstrings em todas as classes e métodos públicos
- Funções com responsabilidade única (Single Responsibility)
- Classes pequenas e coesas

### Requisitos de Performance

- Jogo deve suportar múltiplas partidas simultâneas
- Baixa latência em jogadas (sub-second response)
- Memory-efficient para rodar em ambientes restritos

## Fluxo de Desenvolvimento

### Estratégia de Branches

- Feature branches a partir de main
- Nomeclatura: feature/descripcion-kb
- Pull requests obrigatórios para merge em main
- Code review com no mínimo 1 aprovações

### Processo de Revisão

- Todos os PRs devem verificar compliance com a constituição
- Tests devem passar antes de review
- Codeowners podem solicitar mudanças
- Complexidade deve ser justificada no PR

### Gates de Qualidade

- Tests passing: todos os testes unitários e de integração
- Coverage: mínima 80% de cobertura
- Linting: zero erros e warnings
- Documentation: ADRs atualizados quando aplicável

## Governança

Constituição superseda todas as outras práticas do projeto.

- Alterações requerem documentação, aprovação e plano de migração
- Todos os PRs/vérificacoes devem verificar compliance
- Complexidade deve ser justificada
- Esta constituição guia o desenvolvimento do projeto Domino Amazonense

### Registro de alteração — 2026-09-30

Definições confirmadas pelo responsável pelo projeto: modo único de quatro jogadores em duplas; bônus de cinco carroças condicionado à aceitação e nova distribuição das 28 pedras sem bônus em caso de recusa; galo (passe geral) vale somente 50 pontos para a última dupla que jogou e não encerra a raia; segundo passe consecutivo não pontua; abertura após tranca com 6-6; tranca e batida normal concedem a soma das mãos adversárias arredondada para baixo ao múltiplo de 5. Documentação e backlog atualizados; implementação do motor permanece pendente.

**Versão**: 1.0.1 | **Aprovada em**: 2026-09-30 | **Última Alteração**: 2026-09-30
