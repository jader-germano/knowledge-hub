# Infrastructure Fixes & Patterns (2026-03-12)

## pi-watchdog — Critical Fixes Applied
- BUG: `brew services restart ollama` fails in LaunchAgent (brew not in PATH)
  FIX: Add `/opt/homebrew/bin` to PATH in plist EnvironmentVariables
- BUG: `node server.js &` spawns orphan processes without PID guard
  FIX: Use `launchctl kickstart gui/$(id -u)/com.jader.pi-local` instead
- BUG: Watchdog checking health via curl then spawning node — races with KeepAlive
  FIX: Check launchctl PID, only kick if PID missing

## LaunchAgent Patterns
- Use `launchctl kickstart` not manual process spawn for managed services
- `KeepAlive=true` + `ThrottleInterval` handles restarts — don't duplicate in watchdog
- Always set full PATH in EnvironmentVariables (brew, nvm, user bin)
- Error logs persist from old runs — clear before testing fix: `> /tmp/service.error.log`

## Ollama LAN Access
- Default bind: localhost only
- Fix: `OLLAMA_HOST=0.0.0.0:11434` in `~/Library/LaunchAgents/homebrew.mxcl.ollama.plist`
  under `<key>EnvironmentVariables</key>`
- After edit: `launchctl unload` + `launchctl load` (stop/start not enough)
- Verify: `lsof -i :11434 | grep LISTEN` → should show `TCP *:11434`

## VPS SSH
- Key: `~/.ssh/id_ed25519` (ED25519)
- Pub: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJiVGTYizouAA5+ZWMJnZM/R4jLfetj5VUAcH64BrhIf`
- Fix when rejected: hPanel Console → `echo "<pubkey>" >> ~/.ssh/authorized_keys`
- VPS was disk-full (100%) — resolved via hPanel console docker prune

## Memory Base Integrity
- Seal checksums after every major session: `md5 ~/PI_MEMORY.md`
- Current 00-owner-core.md MD5: `1dfae8b19aead81be3d0ea59697de845`
- AwesomePie daemon overwrites `_Last updated:` line every 10 min — checksums drift
  → Re-seal after daemon edits PI_MEMORY.md
