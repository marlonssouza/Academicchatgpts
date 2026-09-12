# OpenManus Academic

Aplicação independente para fornecer capacidades de execução acadêmica aos GPTs **Orientador Acadêmico UNDB** e **Coach TCC**.

Este projeto é deliberadamente separado do SaaS jurídico. Não deve acessar clientes, processos, tenants, banco do escritório ou qualquer dado operacional do DigitalIA.

## Modos

- `tcc`: coerência entre projeto, problema, objetivos, método, capítulos e conclusão
- `case`: análise de CASE jurídico
- `paper`: análise de PAPER jurídico
- `abnt`: auditoria de citações e referências
- `references`: verificação de referências e dados ausentes
- `compare`: comparação de versões e documentos
- `research`: pesquisa acadêmica verificável

## API

- `GET /health`
- `GET /modes`
- `POST /v1/academic/run`
- `GET /openapi.json`
- `GET /privacy`

A API usa `X-API-Key`, configurada pela variável `ACADEMIC_API_KEY`.

## GPT Actions

Depois do deploy HTTPS:

1. Abra o editor do GPT existente.
2. Adicione uma Action.
3. Configure autenticação por API key usando o cabeçalho `X-API-Key`.
4. Importe `https://SEU-DOMINIO/openapi.json`.
5. Teste a operação `runAcademicTask`.

O Orientador Acadêmico UNDB deve priorizar `case`, `paper`, `abnt`, `references` e `research`.
O Coach TCC deve priorizar `tcc`, `compare`, `abnt`, `references` e `research`.

## Deploy

O projeto inclui `render.yaml`, mas deve ser implantado como serviço próprio. Não reutilize o serviço Render do SaaS jurídico.
