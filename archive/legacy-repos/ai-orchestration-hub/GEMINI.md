# GEMINI.md

This file provides instructional context for Gemini CLI when working in Jader Phelipe Germano's workspace.

## Project Overview

This is a comprehensive development environment for a Senior Software Engineer, primarily focused on **TSE (Tribunal Superior Eleitoral)** projects and personal full-stack applications.

### Key Projects

#### 🏛️ Banco de Docentes da EJE (TSE) - `~/code/tse/`
The main professional project, a system for managing judicial teaching staff.
- **Backend (`docentes-backend`):** Spring Boot 3, Java 21, MyBatis, Oracle Database.
- **Frontend (`docentes-frontend`):** Angular workspace with shared libraries.

#### 💈 GoBarber (Personal) - `~/code/pessoal/`
A full-stack barber scheduling application.
- **Backend:** Node.js, Express, TypeScript, TypeORM, PostgreSQL.
- **Web Frontend:** React, Vite, styled-components.
- **Mobile App:** React Native, Expo, expo-router.

#### 🤖 Automation & Skills - `~/`
- **Skill Files:** Custom `.skill` files/folders used for task automation (e.g., `relatorio-atividades-digisystem-mensal`).
- **Monthly Reports:** Automated Jira data extraction and Google Sheets population via Apps Script for Digisystem.

---

## Environment & Tooling

- **OS:** macOS (zsh + Oh My Zsh)
- **Node.js:** Managed via `nvm`. Use `.nvmrc` files in project roots.
- **Java:** Managed via `sdkman`. Java 21 is required for TSE projects.
- **Package Managers:**
  - `pnpm`: Used for `docentes-frontend`.
  - `yarn`: Used for `backend-goBarber` and `frontend-gobarber`.
  - `npm`: Fallback and global tools.
- **CLI Tools:** Angular CLI (`ng`), Expo CLI (`expo`), Maven (`mvn`).

---

## Building and Running

### TSE Projects
| Task | Command |
| :--- | :--- |
| **Backend Build** | `mvn clean package -DskipTests` |
| **Backend Run** | `mvn spring-boot:run -Dspring-boot.run.profiles=dsv` |
| **Frontend Dev** | `pnpm start` |
| **Frontend Build** | `pnpm run release-local` |

### GoBarber Projects
| Task | Command |
| :--- | :--- |
| **Backend Dev** | `yarn dev:server` |
| **Frontend Dev** | `yarn dev` |
| **Mobile Dev** | `expo start` |
| **Database (Postgres)**| `docker compose up -d db` |

---

## Development Conventions

- **Surgical Changes:** Adhere to the existing architecture of each project (Layered for TSE, Domain-Driven for GoBarber).
- **LGPD (TSE Backend):** Always call `logLGPDService.logarDados()` in admin endpoints that handle personal data. Wrap in `try/catch` to avoid propagating log failures to users.
- **Testing:**
  - TSE Backend: `mvn test`
  - GoBarber Backend: `yarn test` (Jest)
  - TSE Frontend: `pnpm run lint`
- **Automation:** Refer to `memoria-relatorio-digisystem.md` for specifics on the monthly reporting workflow and Jira/Google Sheets integration.
- **Coding Style:** Follow the patterns established in `CLAUDE.md` and project-specific `README.md` files.


## AgentOps Execution Hierarchy
1. Skill-first
2. Specialist agent
3. Tool execution
4. Manual fallback

## Skill vs Agent Decision Rule
- Skill for repeatable, standardized workflows.
- Agent for orchestration, multi-step strategy, and trade-offs.

## Mandatory Agent Output Contract
All agents should return:
- selected_specialists / plan
- deliverables
- quality_gates
- memory_delta
- next_action

## Memory Hygiene
- Stable knowledge (long-lived)
- Session working memory (temporary)
- Archive/imported snapshots (historical)
