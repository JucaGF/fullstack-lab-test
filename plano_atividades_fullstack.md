# Atividades para casa — Full Stack do Trilha

## Escopo e decisões

Este documento estrutura **quatro entregas semanais para casa** em um projeto contínuo de eventos universitários. Cada entrega se apoia na anterior, acrescenta uma funcionalidade central e é concluída quando os testes públicos acumulados passam. O planejamento dos encontros presenciais e o mini-projeto de encerramento ficam fora deste documento.

O ciclo acompanha esta ordem: introdução ao back-end; introdução a banco de dados; integração entre back-end e banco; introdução ao front-end. As tecnologias escolhidas são FastAPI/Python, SQLite com SQLAlchemy e JavaScript/React. O uv gerencia as dependências Python; o npm gerencia as dependências do frontend. A turma está no começo do curso, já teve contato com Git e terá seu primeiro contato com desenvolvimento web neste bloco. Há um encontro por semana; o trabalho em casa ocorre até o seguinte. IA é permitida, com orientação no repositório.

O sistema cresce em uma única história: **publicar eventos → representar inscrições no banco → inscrever pela API → inscrever pela interface**. Não há autenticação, deploy, cancelamento nem CRUD completo neste ciclo. O usuário selecionado na interface é um usuário de demonstração criado pelo seed; não representa login.

## Contratos estáveis do projeto

Os nomes abaixo são públicos porque o material novo e os testes dependem deles. O aluno mantém liberdade para organizar a lógica interna.

| Entidade | Campos obrigatórios | Regras |
| --- | --- | --- |
| `Event` / tabela `events` | `id`, `title`, `date`, `capacity` | `title` não fica vazio; `capacity > 0`; `date` é uma data ISO (`AAAA-MM-DD`). |
| `User` / tabela `users` | `id`, `name`, `email` | `id` identifica o usuário de demonstração usado nos testes. |
| `Registration` / tabela `registrations` | `event_id`, `user_id` | Cada par evento/usuário aparece no máximo uma vez; ambos referenciam registros existentes. |

| API | Introduzido em | Contrato observável |
| --- | --- | --- |
| `GET /events` | Starter da entrega 1 | Lista eventos. A rota permanece nas quatro entregas. |
| `GET /events/{event_id}` | Starter da entrega 1 | Retorna o evento ou 404. |
| `POST /events` | Entrega 1 | Recebe `title`, `date`, `capacity`; responde 201 com ID e dados criados; entrada inválida retorna erro de validação. |
| `POST /events/{event_id}/registrations` | Entrega 3 | Recebe `user_id`; sucesso retorna 201; evento ou usuário ausente retorna 404; duplicidade ou falta de vagas retorna 409. |

Na entrega 3, as respostas de evento passam a incluir `available_slots`, calculado a partir de `capacity` e do número de inscrições. Uma inscrição válida reduz esse valor em um. Nenhum teste da entrega 1 deve exigir que o armazenamento continue em memória nem comparar o JSON por igualdade exata, porque a implementação e a resposta evoluem depois.

## Como o GitHub funciona

O professor publica no repositório oficial. Cada aluno cria um fork e trabalha em uma branch permanente chamada `aluno` no próprio fork:

```text
oficial/main → fork/main → fork/aluno
  publicação    espelho      implementação do aluno
```

No setup inicial, o aluno clona seu fork, adiciona o repositório oficial como remote `upstream`, cria `aluno` a partir de `main`, habilita GitHub Actions no fork e confere a primeira execução após um push. O workflow já vem no starter e executa os testes em pushes para `aluno`. O README final terá os comandos exatos, URLs e imagens curtas apenas nos pontos da interface do GitHub que precisarem delas.

Comandos de referência para o README, usando URLs reais na publicação:

```bash
git clone <url-do-fork>
cd fullstack-lab
git remote add upstream <url-do-repositorio-oficial>
git switch -c aluno
git push -u origin aluno
```

Antes de sincronizar, o aluno conclui ou guarda qualquer alteração local em andamento. A atualização semanal segue este fluxo:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
git switch aluno
git merge main
git push origin aluno
```

O `--ff-only` faz a atualização parar se `fork/main` tiver trabalho próprio; nesse caso o aluno pede ajuda para resolver a situação sem apagar commits. O README explicará onde habilitar Actions no fork e como localizar a execução correspondente ao último push.

Quando uma etapa nova sai, o aluno atualiza `fork/main` com `oficial/main`, faz merge de `main` em `aluno`, lê o documento do checkpoint, executa os testes, implementa, faz commit e push em `aluno`, e confere o Actions. Ele só avança depois que os testes acumulados passam. Não há PR obrigatório nem correção manual de cada entrega.

Professor acrescenta documentação, testes e scaffolding em `oficial/main`; aluno modifica a implementação na branch `aluno`. O professor evita publicar mudanças nos arquivos que a atividade anterior pediu ao aluno para editar. Se uma conexão nova exigir mudança nesses arquivos, o enunciado instrui **o aluno** a fazê-la. Cada checkpoint identifica arquivos para ler, para alterar e para preservar. A divisão é por checkpoint, sem pastas artificiais de professor e aluno.

## Pacote publicado a cada semana

Cada liberação acrescenta:

1. `docs/checkpoint-XX.md`: problema, objetivo, comportamento esperado, exemplos de entrada e saída, arquivos para ler/alterar/preservar, sequência sugerida, dicas graduais, testes e critério de conclusão.
2. Arquivos novos de scaffolding: apenas o necessário para a nova parte rodar, com comentários explicando propósito, entradas, saídas e pontos de extensão.
3. Testes públicos da funcionalidade nova, mantidos junto dos testes anteriores.
4. Dados de exemplo reproduzíveis quando a etapa precisar deles.

O `README.md` é o guia permanente de setup, Git, execução, testes e solução de problemas, com um link para o checkpoint atual. `AGENTS.md` e `CLAUDE.md` entram no starter e mantêm regras gerais para agentes; detalhes da semana ficam no checkpoint. O workflow do Actions e o comando local de testes são definidos no starter e permanecem estáveis para o aluno.

## Entrega 1 — API de eventos em memória

**Problema:** a organização precisa cadastrar eventos e consultá-los por HTTP. A listagem e a busca por ID já vêm funcionando; falta a criação.

**Professor fornece:** aplicação FastAPI executável, armazenamento em memória, `GET /events`, `GET /events/{event_id}`, exemplos de JSON e chamadas HTTP, teste inicial passando, estrutura da rota de criação e comando único de testes. Não exigir que o aluno configure o framework do zero.

**Aluno constrói:** `POST /events`; valida título não vazio, data válida e capacidade positiva; cria ID, guarda o evento e responde 201. O código da rota e da validação fica sob responsabilidade do aluno nas etapas posteriores.

**Testes públicos:** evento válido retorna 201 e aparece em GET; IDs distintos são atribuídos a criações distintas; título vazio, data inválida e capacidade zero ou negativa são rejeitados; GET por ID inexistente retorna 404. Os testes criam seu próprio estado para não depender de ordem de execução.

**Passagem:** rotas e forma de evento são conhecidas pela entrega 2. Nenhum teste exige perda de dados após reinício; essa observação pode motivar a próxima atividade, mas a implementação será trocada na entrega 3.

## Entrega 2 — Modelo de inscrições no banco

**Problema:** eventos e inscrições precisam existir de forma persistente, com relações e restrições que impeçam dados incoerentes. O banco entra no mesmo repositório; a API ainda usa memória nesta entrega.

**Professor fornece:** conexão e inicialização simples do SQLite, base declarativa do SQLAlchemy, comando para recriar um banco local, seed com usuários/eventos e testes que usam um banco temporário. A verificação de chaves estrangeiras fica habilitada em todas as conexões; sem isso, uma referência inválida poderia ser aceita no SQLite.

**Aluno constrói:** modelos `Event`, `User` e `Registration` com os campos públicos, chaves e restrições; uma consulta SQL curta que lista os participantes de um evento. O exercício central é representar a inscrição como relação entre usuário e evento e impedir a duplicidade no banco.

**Testes públicos:** tabelas são criadas em banco vazio; um evento e um usuário podem ser inscritos; um mesmo usuário não pode ser inscrito duas vezes no mesmo evento; referências inexistentes e capacidade inválida são rejeitadas; a consulta retorna os participantes esperados. Os testes da API da entrega 1 continuam passando.

**Passagem:** a entrega 3 usa os mesmos modelos, sem pedir que o aluno redesenhe o esquema. Nomes de tabelas e colunas essenciais são contrato explícito para o scaffolding seguinte.

## Entrega 3 — Inscrição pela API com persistência

**Problema:** a API e o banco, até aqui separados, precisam formar um fluxo único. Uma inscrição só deve acontecer quando evento e usuário existem, o usuário ainda não está inscrito e há vaga.

**Professor fornece:** integração da sessão do banco com FastAPI, seed reproduzível, um exemplo de consulta com SQLAlchemy e arquivo novo para a rota de inscrição. Esses arquivos são acrescentados sem sobrescrever as rotas que o aluno alterou na entrega 1.

**Aluno constrói:** adapta as rotas de eventos para ler/gravar no banco; implementa a inscrição usando os modelos da entrega 2; devolve `available_slots` nas respostas de evento; aplica 404 e 409 conforme o contrato. A regra de vagas usa a quantidade de inscrições persistidas. O aluno faz a conexão entre a rota anterior e a infraestrutura nova.

**Testes públicos:** todos os testes HTTP anteriores continuam passando; evento criado é encontrado por uma nova instância da aplicação usando o mesmo banco; inscrição válida é persistida e reduz vagas; evento e usuário ausentes retornam 404; inscrição repetida e evento lotado retornam 409 sem acrescentar outra linha. Os testes criam e isolam seu próprio banco.

**Passagem:** a entrega 4 consome apenas o contrato HTTP. A interface não acessa SQLite diretamente.

## Entrega 4 — Inscrição pela interface

**Problema:** um usuário precisa ver eventos e inscrever-se sem conhecer rotas HTTP. A interface deve mostrar o estado real da operação.

**Professor fornece:** projeto React executável, layout, estilos, componente visual de evento, seleção de usuários de demonstração compatível com o seed e exemplo mínimo de chamada à API. Não há setup de autenticação nem trabalho de CSS como requisito da atividade.

**Aluno constrói:** busca a lista de eventos na API, renderiza vagas, envia a inscrição do usuário escolhido e atualiza o resultado. Mostra carregamento, lista vazia, sucesso e erro. Desabilita a ação enquanto a requisição está em andamento para evitar envio repetido. O estado exibido após sucesso vem de uma nova resposta do servidor.

**Testes públicos:** a interface renderiza os eventos recebidos; mostra carregamento antes da resposta e erro quando a API falha; envia a inscrição correta; impede dois envios simultâneos; após sucesso, mostra a nova quantidade de vagas; após falha, não anuncia sucesso. A suíte acumulada também roda os testes de API e banco.

## Testes e critério de conclusão

Um único comando local e o workflow do Actions executam a suíte acumulada. Após incorporar uma liberação, falhas dos testes novos são esperadas: elas mostram o comportamento ainda não construído. O checkpoint está pronto quando todos os testes passam na branch `aluno` e o Actions do fork confirma o mesmo commit. Os testes verificam comportamento e integridade observável, sem impor nomes de funções internas ou camadas extras.

Como não há correção manual rotineira, os testes precisam cobrir sucesso, entradas inválidas e erros importantes que estejam descritos no enunciado. Não há testes secretos necessários para esta finalidade. O aluno é orientado a não alterar testes, seed ou workflow para obter verde; se encontrar um teste incorreto, registra o caso e pede revisão ao professor ou monitor.

Antes de publicar cada checkpoint, o professor verifica: starter executa com os comandos documentados; testes antigos continuam passando sobre uma solução da etapa anterior; novos testes falham apenas pelo comportamento ainda não implementado; solução de referência passa a suíte completa; merge sobre uma branch fictícia de aluno funciona; e o Actions foi testado em um fork de ensaio. O material do professor pode ficar em branch privada até a liberação.

## Documentação para alunos e agentes

**README permanente:** visão curta do projeto; ferramentas necessárias; setup de Python e JavaScript; como executar API, banco, interface e testes; fork, `upstream`, branch `aluno`, sincronização semanal e habilitação de Actions; link do checkpoint atual; perguntas de diagnóstico para pedir ajuda. Os comandos exatos serão preenchidos quando o starter executável existir, nunca inventados antes disso.

**Documento de checkpoint:** abre pelo problema e resultado visível; mostra um exemplo de sucesso e um erro; diz o que veio pronto e o que o aluno modifica; oferece uma sequência sugerida sem impor arquitetura interna; lista testes e a condição de conclusão; tem dicas graduais para quem travar. Não inclui a solução de referência.

**Comentários no código:** explicam a responsabilidade do módulo e o contrato do ponto que o aluno vai completar. Evitam narrar linha por linha e não resolvem a tarefa por antecipação. Um aluno deve conseguir localizar o início do trabalho pelo enunciado e pelos comentários.

**`AGENTS.md` na raiz:** instruções curtas e estáveis para qualquer agente que o leia: consultar README e checkpoint vigente; explicar o fluxo e os arquivos afetados antes de editar; respeitar os contratos públicos; preservar o trabalho anterior; não editar testes, seed ou workflow para produzir verde; fazer mudanças focadas; executar o comando completo de testes; relatar falhas com honestidade; resumir em linguagem acessível o que mudou e por quê. IA pode implementar código quando o aluno solicitar. Essas instruções orientam o agente; os testes verificam o comportamento.

**`CLAUDE.md` na raiz:** importa `AGENTS.md` e contém apenas alguma instrução específica de Claude Code que venha a ser necessária. Isso mantém uma fonte principal de guardrails e evita divergência entre ferramentas. O guia humano continua no README, para funcionar também com outras IAs ou sem IA.

## Ordem de produção do material

1. Criar starter da entrega 1 com README, instruções de agente, testes e workflow.
2. Implementar uma solução fictícia de aluno para a entrega 1.
3. Preparar a entrega 2 em branch do professor e testar o merge na solução fictícia.
4. Repetir a simulação para as entregas 3 e 4, incluindo uma solução alternativa válida quando houver risco de o scaffolding depender de detalhes internos.
5. Publicar cada pacote na `main` oficial apenas na semana correspondente, marcado por uma tag de checkpoint.

Este documento define atividades e operação do projeto. Não substitui o roteiro de nenhum encontro presencial nem prescreve o projeto de encerramento do bloco.
