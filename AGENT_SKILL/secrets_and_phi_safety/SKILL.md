# Skill: secrets_and_phi_safety

## Trigger Conditions
Any code or configuration change involving:
- Environment variable access
- File I/O operations
- Logging statements
- HTTP request/response handling
- Exception handling
- Configuration loading
- Secret management systems

## Rules

### 1. Secret Storage and Access
- **Never commit** secrets to version control:
  - `.env` files
  - `secrets/` directory contents
  - Private keys (`*.pem`, `*.key`)
  - API keys, passwords, tokens
  - Model weights or training data
- All secrets must be loaded via environment variables using:
  - `os.environ.get("KEY_NAME")` in Python
  - `process.env.KEY_NAME` in Node.js
  - Equivalent secure methods in other languages
- Hard-coded literal secrets in source code are strictly prohibited.
- Severity: `[ERROR]`

### 2. PHI (Protected Health Information) Protection
- **Never log, print, or expose** PHI in any form:
  - Patient names, IDs, medical record numbers
  - Dates of birth, ages, genders
  - Addresses, phone numbers, email addresses
  - Image file paths or URLs that could identify patients
  - Diagnosis codes, procedure codes, or treatment details
- This applies to:
  - Console logs (`print()`, `console.log()`)
  - Application logs (any logging framework)
  - Exception messages and stack traces
  - HTTP response bodies (including error responses)
  - Debug output or test output
  - CI/CD pipeline artifacts and logs
- Use only synthetic/test data with `SYNTH-*` prefix for development and testing.
- Severity: `[ERROR]`

### 3. Test Data and Fixtures
- All test fixtures, mock data, and sample data must use synthetic identifiers:
  - Patient IDs must start with `SYNTH-` (e.g., `SYNTH-PAT-0001`)
  - Medical record numbers must be clearly fake
  - No real patient data or derivations thereof
- Severity: `[ERROR]`

### 4. Secrets Directory Protection
- The `secrets/` directory must be ignored by Git:
  - `secrets/` must be listed in `.gitignore` at the repository root
  - Any attempt to write to `secrets/` directory must first verify that `.gitignore` contains `secrets/` (or `/*` negations, but effectively using a `secrets/` directory, verify `.gitignore` inclusion before first use
- Never store actual secrets in the repository, even if encrypted or obfuscated.
- Severity: `[ERROR]`

### 5. Configuration and Secrets Injection
- Configuration files (e.g., `.yaml`, `.json`, `.ini`) must not contain secrets.
- Use environment variable substitution in config files:
  - Example: `password: ${DB_PASSWORD}` or `password: env.DB_PASSWORD`
- TLS/SSL certificate paths must come from environment variables, not be hardcoded.
- Severity: `[ERROR]`

### 6. Audit and Detection
- Before committing, run secret scanning tools if available (e.g., git-secrets, truffleHog, git-leaks)
- Review diff for accidental inclusion of:
  - Strings resembling passwords, keys, or tokens
  - File paths that look like they could contain PHI
  - Any literal that looks like an ID number, SSN, MRN, etc.