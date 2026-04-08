# Cloudflare Email Structure

## Current Direction

- Primary mailbox target: `jader@jpglabs.com.br`
- Planned mail runtime: `docker-mailserver` on the JPGLabs VPS
- Cloudflare role: DNS authority for `jpglabs.com.br` and DNS-01 support for certbot
- Current local evidence does not show a completed migration to Cloudflare Email Routing as the main mail host

## Records Already Planned

- `A mail.jpglabs.com.br -> 187.77.227.151` (`DNS only`)
- `MX @ -> mail.jpglabs.com.br` priority `10`
- `TXT @ -> v=spf1 mx ~all`
- `TXT _dmarc -> v=DMARC1; p=quarantine; rua=mailto:jader@jpglabs.com.br`
- `TXT mail._domainkey -> live DKIM key published in DNS`

## Operational Notes

- The documented completion flow is still `bash /docker/mailserver/finish-setup.sh` on the VPS.
- Live DNS already answers with MX, SPF, DMARC, and DKIM for `jpglabs.com.br`.
- Public probes on 2026-03-31 still timed out on ports `25`, `465`, `587`, and `993`, so the remaining blocker is service reachability on the host path, firewall path, or Hostinger network path.

## Status At 2026-03-31

- Cloudflare is acting as DNS/control plane, not as the active mailbox provider.
- The mailbox plan for `jader@jpglabs.com.br` is incomplete until:
  - the VPS mail setup finishes
  - IMAP/SMTP login is verified
  - send/receive succeeds end to end
