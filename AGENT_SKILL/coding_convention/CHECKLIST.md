# Checklist: coding_convention

Instructions: For each item below, mark whether the change complies with the rule.

## Python Conventions
- [ ] File names use snake_case (e.g., `patient_service.py`)
- [ ] Class names use PascalCase (e.g., `PatientService`)
- [ ] Function and variable names use snake_case (e.g., `get_patient_by_id`)
- [ ] Constants use UPPER_SNAKE_CASE (e.g., `MAX_PATIENTS_PER_PAGE`)
- [ ] Line length does not exceed 100 characters
- [ ] Every public function, class, and module has a docstring
- [ ] Docstrings follow Google/NumPy style (Args, Returns, Side Effects)
- [ ] No `print()` statements; logging is used instead
- [ ] Exceptions are typed and not overly broad (avoid bare `except:`)
- [ ] FastAPI routers use `APIRouter(prefix=...)`

## TypeScript/React Conventions
- [ ] File names use snake_case (e.g., `patient_list.tsx`)
- [ ] Component names use PascalCase (e.g., `PatientList`)
- [ ] Hook names use `useSnakeCase` (e.g., `usePatientData`)
- [ ] Follows Airbnb JavaScript/TypeScript style guide
- [ ] No `console.log()` in production code (use proper logging)

## Error Handling
- [ ] No `print()` or `console.log()` for error reporting
- [ ] Errors are logged at appropriate level (debug/info/warn/error)
- [ ] Custom exceptions are used where appropriate
- [ ] Exceptions are not swallowed without handling

## RBAC
- [ ] Only use role constants: `RO_RADIOLOGIST`, `RO_THERAPIST`
- [ ] No hard-coded role strings in conditionals
- [ ] Role checks are centralized where possible

## Configuration
- [ ] No hard-coded endpoints, API keys, or configuration values
- [ ] Configuration loaded via environment variables or secrets/
- [ ] `secrets/` directory is properly gitignored
- [ ] No secrets in code, logs, or comments

## Commit Messages
- [ ] Commit message follows Conventional Commits format
- [ ] Type is one of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- [ ] Scope is provided when applicable
- [ ] Subject is imperative, lowercase, no trailing period