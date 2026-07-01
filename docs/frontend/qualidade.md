# Qualidade de Código

## Status Atual
O projeto passou pela verificação de análise estática do **ESLint (v9)** e encontra-se em conformidade com todas as regras definidas.

* **Resultado da última auditoria:** 0 erros e 0 avisos encontrados.
* **Escopo da análise:** Todo o código fonte (`.js`, `.jsx`) e documentação (`.md`).
* **Configuração:** O padrão de qualidade é mantido via `eslint.config.js` na raiz do projeto.

## Política de Qualidade
Para manter este nível de qualidade, todo novo código deve ser verificado antes de ser enviado ao repositório:
1. Rode o comando `npm run lint`.
2. Se houver erros, utilize `npx eslint . --fix` para correção automática.
3. O deploy do projeto (via GitHub Actions) está configurado para validar a integridade do código.