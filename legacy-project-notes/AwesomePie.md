# 🥧 AwesomePie

> Native Swift AI assistant — macOS menubar + iOS companion  
> No Electron. No external dependencies. Pure Apple SDK.

---

## Repos
- Mac: `~/code/pessoal/awesomepie/`
- iOS: `~/code/pessoal/awesomepie-ios/`

## Fallback Chain

```
1. Local Ollama      localhost:3131         qwen2.5-coder:7b
2. Local Ollama      localhost:3131         llama3.2:3b
3. VPS               api.jpglabs.com.br     deepseek-r1:7b
4. OpenAI            api.openai.com         gpt-4o
5. OpenAI            api.openai.com         gpt-4o-mini
6. Gemini            googleapis.com         gemini-2.0-flash
7. Gemini            googleapis.com         gemini-1.5-pro
8. Anthropic         api.anthropic.com      claude-sonnet-4-6 ✅
```

## Status

| Component | Status |
|-----------|--------|
| Mac ChatService | ✅ Direct API — no subprocess |
| iOS ChatService | ✅ Direct API + VPS tier |
| iOS SettingsView | ✅ Written |
| Mac build | 🔴 Blocked — Xcode license |
| iOS .xcodeproj | 🔴 Blocked — xcodegen needs Xcode license |

## Build Commands (after `sudo xcodebuild -license accept`)

```bash
# Mac
cd ~/code/pessoal/awesomepie && swift build

# iOS — generate project
cd ~/code/pessoal/awesomepie-ios && xcodegen generate
# Then open .xcodeproj in Xcode
```

## Links
- `legacy-project-notes/VPS-Infrastructure.md` — VPS tier 3
- `projects/pi-local-app/PROJECT_CONTEXT.md` — local tiers 1-2
