# Skill: coding_convention

## Trigger Conditions
Any code edit or creation (files with extensions: .py, .js, .ts, .tsx, .java, .cpp, .h, etc.)

## Rules

### 1. Python Conventions
- Follow PEP 8 with line length ≤ 100 characters
- Use `ruff`-compatible formatting
- Class names: `PascalCase`
- Function and variable names: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- FastAPI routers should be grouped under `APIRouter(prefix=...)`
- Every public function, class, and module must have a docstring:
  - Purpose: brief description
  - Parameters: list with types and descriptions
  - Return: return type and description
  - Side-effects: note any side effects (if applicable)
- Severity: `[ERROR]`

### 2. TypeScript/JavaScript Conventions
- Follow Airbnb JavaScript Style Guide
- Use ESLint with `eslint-config-airbnb` as base
- Component names: `PascalCase`
- Hook names: `useSnakeCase` (e.g., `useUserData`)
- File names: `snake_case.tsx` or `snake_case.ts`
- Use TypeScript strict mode
- Prefer interfaces over types for object shapes
- Export constants as `const` in UPPER_SNAKE_CASE
- Severity: `[ERROR]`

### 3. Error Handling
- Never use `print()` for logging or debugging
- Use appropriate logging levels: `debug`, `info`, `warn`, `error`
- Raise typed exceptions (custom exceptions preferred over generic Exception)
- Handle exceptions at appropriate levels; do not swallow exceptions silently
- Severity: `[ERROR]`

### 4. RBAC (Role-Based Access Control)
- Use only declared role constants for permission checks:
  - `RO_RADIOLOGIST` (Read-Only Radiologist)
  - `RO_THERAPIST` (Read-Only Therapist)
- Do not hard-code role strings in conditionals
- Severity: `[ERROR]`

### 5. Configuration Management
- No hard-coded endpoints, API keys, or configuration values
- Load configuration from environment variables via `os.environ.get()` (Python) or `process.env` (Node.js)
- Secrets must be loaded from the `secrets/` directory or environment variables only
- Severity: `[ERROR]`

### 6. Commit Messages
- Follow Conventional Commits format: `<type>(<scope>): <subject>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- Scope should be the module or component affected (optional but recommended)
- Subject should be imperative, lowercase, no trailing period
- Body and footer optional but recommended for complex changes
- Severity: `[WARN]`