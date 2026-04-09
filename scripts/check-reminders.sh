#!/bin/bash
# check-reminders.sh — Lista lembretes pendentes e exibe notificação macOS
# Executado automaticamente via launchd às 08:00 e 19:00

REMINDERS=$(osascript <<'SCRIPT'
tell application "Reminders"
  set pendingList to {}
  repeat with r in (every reminder whose completed is false)
    set end of pendingList to name of r
  end repeat
  if length of pendingList is 0 then
    return "Nenhum lembrete pendente."
  else
    set output to ""
    repeat with i from 1 to length of pendingList
      set output to output & "• " & item i of pendingList
      if i < length of pendingList then
        set output to output & linefeed
      end if
    end repeat
    return output
  end if
end tell
SCRIPT)

COUNT=$(osascript -e 'tell application "Reminders" to count (every reminder whose completed is false)' 2>/dev/null || echo "0")

HOUR=$(date +%H)
if [ "$HOUR" -lt 12 ]; then
  GREETING="Bom dia, Jader!"
else
  GREETING="Boa noite, Jader!"
fi

osascript <<NOTIFY
display notification "$REMINDERS" with title "$GREETING" subtitle "$COUNT lembrete(s) pendente(s)" sound name "Ping"
NOTIFY
