# Session Memory - 2026-03-10 - User Engineering Scope and Docs-First

## Working Preferences
- Confirm target file or component before editing when the request is ambiguous.
- Break instructions into clear steps and show planned touch points before making changes.
- Review proposed changes with `brutal-critic-triad.md` before implementation.
- Keep scope strict; do not redesign, restyle broadly, or refactor laterally without explicit approval.
- Treat tests as part of every behavior change. Update or add them, or state why no test applies.
- Prefer official current documentation and project-pinned versions over recalled knowledge for technical concepts and patterns.

## Confirmed Technical Profile
- Primary delivery lane: Java 21, Spring Boot 3.x, Spring Security 6, Spring Data JPA/Hibernate, MyBatis, Oracle, Angular 17+, TypeScript, RxJS, Angular Material, PrimeNG, Tailwind CSS.
- Complementary lane: Node.js, React, Vite, Docker, Kubernetes, GitHub Actions, GitLab CI, Jenkins, SonarQube, JaCoCo, n8n, MCP.
- Design and architecture patterns: SOLID, Clean Code, Clean Architecture, DDD, Hexagonal Architecture, CQRS, Event Sourcing, layered architecture where already established.

## Carry-Forward Architecture
- JPGLabs backend direction is resolved:
  - keep Node active and improve it with reactive/evented scaling patterns
  - create a separate Java/WebFlux replica behind the same load balancer
  - maintain dual-service parity for contract changes
- After systems stabilization and documentation closure, the next priority is the mobile app consuming the load-balanced Node+Java edge.
