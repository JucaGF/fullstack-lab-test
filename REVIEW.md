# Guia de revisão — atividades Full Stack do Trilha

Este repositório é uma cópia temporária para revisão. O [planejamento](plano_atividades_fullstack.md) descreve as decisões pedagógicas; o [README](README.md) e os quatro arquivos em `docs/checkpoint-XX.md` são o material que o aluno recebe progressivamente.

## Como ler as branches

| Semana | Starter publicado ao aluno | Solução de referência |
| --- | --- | --- |
| 1 — API em memória | `joaquim/fullstack-checkpoints` | `joaquim/solution-01` |
| 2 — Banco de dados | `joaquim/checkpoint-02` | `joaquim/solution-02` |
| 3 — API e banco | `joaquim/checkpoint-03` | `joaquim/solution-03` |
| 4 — Interface React | `joaquim/checkpoint-04` | `joaquim/solution-04` |

A `main` desta cópia contém a solução final e este guia. Ela existe apenas para facilitar a revisão; não corresponde à `main` do repositório oficial. Os starters deixam os testes novos vermelhos de propósito. Cada solução de referência deve passar todos os testes acumulados até sua semana.

## Executar a solução final

```bash
uv sync --locked
npm ci --prefix frontend
uv run --locked python scripts/check.py
npm run build --prefix frontend
```

Para avaliar a progressão, compare cada starter com o starter da semana anterior e a solução correspondente com seus testes. Vale observar a clareza dos enunciados, o que cada atualização acrescenta ao projeto existente, os contratos dos testes, o fluxo de GitHub nos forks e as orientações em `AGENTS.md`/`CLAUDE.md`.

Registre comentários diretamente nos arquivos ou em pull requests desta cópia. As branches e soluções deste repositório de revisão não devem ser mescladas na `main` oficial.
