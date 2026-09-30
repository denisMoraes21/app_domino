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
- **Galo**: Todos os jogadores passam, inclusive o parceiro
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

Todas as funcionalidades da aplicação devem ser implementadas em Python.

- Usar Python 3.11+ com type hints obrigatórios
- Seguir PEP 8 e PEP 257 para estilo e documentação
- Utilizar virtual environments (venv ou poetry) para isolamento de dependências
- Bibliotecas devem ser autocontidas, testáveis independentemente e bem documentadas

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

- 4 jogadores divididos em 2 duplas (2 jogadores por dupla)
- Cada jogador recebe 7 pedras na distribuição inicial
- O conjunto usado é o duplo-6 (28 pedras totais)
- Partida disputada até 200 pontos ou superior

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

- Batida normal (esvaziar as pedras): conta as pedras do oponente restantes
- Iniciar com 5 carroças: 50 pontos imediato
- Iniciar com 6 carroças: vitória imediata

### Fluxo do Jogo

- Começa quem tem 6-6 (a carroça maior) ou sorteou a peça mais alta
- Jogo evolui no sentido anti-horário (tradicional no Amazonas)
- Objetivo: marcar pontos jogando pedras ou esvaziar a mão para bater
- Pedras devem combinar com as pontas disponíveis na mesa
- Se não tiver jogada disponível (inclusive no início do jogo), o jogador passa
- Ao passar por não ter jogada, a dupla adversária marca 20 pontos
- Se TODOS os jogadores passarem em sequência, chama-se "galo"
- Em caso de galo, a dupla adversária marca 50 pontos automaticamente
- para raias posteriores, quem bateu na ultima rodada é que inicia a partida

### Condições de Vitória

- Partida (jogo longo) termina quando uma dupla atinge 200 pontos
- Uma raia termina quando alguém "bate" (esvazia todas as pedras da mão)
- Bater = não ter mais pedras em posse após jogar a última pedra
- Ao bater, conta-se as pedras restantes dos adversários para pontuação
- Se ninguém bater e o jogo fechar (tranca), ganha quem tem menos pontos na mão
- Em empate de pontos na mão de tranca, perde quem jogou por último
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

**Versão**: 1.0.0 | **Aprovada em**: 2026-09-30 | **Última Alteração**: 2026-09-30
