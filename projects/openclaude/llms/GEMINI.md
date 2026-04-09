# GEMINI Context — OpenClaude

> Gemini implementation details for OpenClaude.

## 1. Contexto

OpenClaude utiliza um shim OpenAI-compatible para suportar o Google Gemini. O CLI permite configurar:
- `CLAUDE_CODE_USE_GEMINI=1`
- `GEMINI_API_KEY` (via Keychain ou env)
- `GEMINI_MODEL=gemini-3-flash` (Conforme escolha do usuário em 2026-04-05)

## 2. Configurações Específicas

Para este workspace:
- **Base URL:** `https://generativelanguage.googleapis.com/v1beta/openai` (padrão de shim do SDK do OpenClaude)
- **Prompting:** Suporte total a Tool Calling nativo (Functions API do Gemini).

## 3. Próximos Passos

- [ ] Validar o modelo `Gemini 3 Flash` no CLI run.
- [ ] Monitorar uso de tokens nas sessões via `cost-tracker.ts`.
- [ ] Confirmar se o keychain do host philipegermano já possui o token necessário.
