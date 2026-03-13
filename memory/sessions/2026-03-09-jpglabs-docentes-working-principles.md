# Session Memory - 2026-03-09 - JPGLabs + Docentes Working Principles

## JPGLabs Carry-Forward Context
- Favor parity across local, Docker, and edge behavior before UI changes.
- Centralize routes and contract points instead of fixing behavior in scattered places.
- Preserve the existing visual language unless a redesign is explicitly requested.
- Validate changes end-to-end with build, lint, runtime, and browser checks, especially for redirects and access control.
- Treat legacy redirects and host/port preservation as product requirements, not incidental details.

## Docentes Carry-Forward Context
- Treat implementation errors as boundary-design failures first, not only as exceptions to silence.
- In LGPD and audit flows, distinguish `titular` from `operador` explicitly; do not infer the titular from the logged-in user when admins or staff inspect third-party data.
- Dedup and audit buffering must key by meaningful behavior surface, not only by coarse identity keys that can hide legitimate logs.
- Centralize sent, skipped, not-confirmed, and failure logging decisions in the service layer instead of spreading them across controllers.
- Any compliance or audit behavior fix needs targeted tests that cover sent, skipped, and failure paths.

## Operating Stance
- Prefer root-cause correction over cosmetic patches.
- Verify behavior in the closest real runtime available when the bug is environment-sensitive.
- Preserve user-visible behavior unless the requirement explicitly changes; fix semantics underneath first.
