# Repository Guidelines

## Project Structure & Module Organization
- `code/tse/docentes-frontend`: Angular workspace. Main app is in `projects/projeto/src`; shared libraries live in `projects/tse/*`.
- `code/tse/docentes-backend/02_fontes`: Spring Boot (Java 21) service. Source is in `src/main/java`; resources in `src/main/resources`; tests in `src/test`.
- `code/pessoal/backend-goBarber`: Node.js + TypeScript API using modular `src/modules/*` and shared infrastructure in `src/shared/*`.
- `code/pessoal/frontend-gobarber`: Vite + React client with UI in `src/components`, route pages in `src/pages`, and hooks/services in `src/hooks` and `src/services`.
- `scripts/`: local utility shell scripts (for example reminder automation).

## Build, Test, and Development Commands
- `cd code/tse/docentes-frontend && npm start`: run Angular app locally (`ng serve projeto`).
- `cd code/tse/docentes-frontend && npm run build && npm run lint`: build libs/app and run lint checks.
- `cd code/tse/docentes-backend/02_fontes && mvn clean test`: run backend unit/integration tests.
- `cd code/tse/docentes-backend/02_fontes && mvn test -Pe2e`: run Selenium tests tagged `e2e`.
- `cd code/pessoal/backend-goBarber && npm run dev:server`: run API in watch mode.
- `cd code/pessoal/backend-goBarber && npm test && npm run build`: run Jest tests and compile TypeScript.
- `cd code/pessoal/frontend-gobarber && npm run dev` (or `npm run build`): run or bundle the React app.

## Coding Style & Naming Conventions
- Respect each module's configured tools: ESLint/Prettier in GoBarber projects, Angular ESLint in `docentes-frontend`.
- `.editorconfig` defaults in GoBarber repos: UTF-8, LF, spaces, 4-space indentation.
- Use `camelCase` for variables/functions, `PascalCase` for classes and React components.
- Java code should keep package names lowercase (for example `br.jus.tse...`) and class names in `PascalCase`.

## Testing Guidelines
- TypeScript tests follow `*.spec.ts` and are usually colocated in `__tests__` folders.
- Angular tests follow `*.component.spec.ts` and `*.service.spec.ts`.
- Java tests follow `*Test.java`; E2E uses JUnit tag `e2e` and the Maven profile `-Pe2e`.
- No global coverage threshold is enforced at workspace level; add or update tests for every bug fix and behavior change.

## Commit & Pull Request Guidelines
- Prefer Conventional Commits patterns seen in history: `feat(scope): ...`, `fix: ...`, `chore: ...`.
- Keep commits focused on one module and one concern.
- PRs should include: concise summary, changed paths, test evidence (commands run), linked issue/ticket (for example `TS1506US-1693`), and screenshots for UI changes.

## 🛠 Engineering Standards (Updated 2026-03-08)
- **High-Availability:** All deployments must use at least 2 replicas for load balancing.
- **Verification:** Every n8n infrastructure workflow must include UX-level verification (Selenium/DOM markers).
- **Documentation:** All solutions must be synced to 'knowledge-hub' repository.
