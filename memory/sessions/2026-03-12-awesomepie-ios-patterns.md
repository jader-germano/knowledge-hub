# AwesomePie iOS — Patterns & Lessons (2026-03-12)

## Speech Recognition
- Use `SFSpeechRecognizer` + `AVAudioEngine` — native, no deps
- `requiresOnDeviceRecognition = true` → Apple Intelligence Neural Engine
- `addsPunctuation = true` → iOS 16+
- NEVER call `recognitionTask?.cancel()` on stop — kills transcript
- Call `recognitionReq?.endAudio()` instead → triggers final result callback
- Always fallback: `finalTranscript ?? liveTranscript` before sending

## Providers
- Default provider: `AIProvider.allCases.first(where: { $0.isAvailable }) ?? .local`
  Never hardcode `.claude` as default — key may not be on device
- Streaming: Claude uses `content_block_delta.delta.text` SSE events
- Streaming: OpenAI uses `choices[0].delta.content` SSE events
- Local timeout: 120s minimum — Ollama cold start can be slow

## Networking
- pi-local must bind to `0.0.0.0` for LAN access from iPhone
- Ollama needs `OLLAMA_HOST=0.0.0.0:11434` in LaunchAgent EnvironmentVariables
- macOS firewall: verify `node` is in Allow list (`socketfilterfw --listapps`)
- iPhone on USB shows as `169.254.x.x` on `en6` — still reaches WiFi IPs

## Keychain
- Store API keys with `kSecClassGenericPassword` — never in source or UserDefaults
- Strip sensitive fields before storing user object: `{ passwordHash: _hash, ...safeUser }`

## Build & Deploy
- Team ID: `RYJN4S9W4U` (Jader Germano Personal Team)
- Device ID: `00008140-00163C303EE1801C` (iPhone do Jader, iOS 26.4)
- After adding new Swift files: always run `xcodegen generate` before build
- Install: `xcrun devicectl device install app --device <id> <path>`
- Launch: `xcrun devicectl device process launch --device <id> <bundleId>`
