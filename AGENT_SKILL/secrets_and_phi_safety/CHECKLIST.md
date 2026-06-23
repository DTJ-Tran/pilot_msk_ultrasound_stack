# Checklist: secrets_and_phi_safety

## Secret Handling
- [ ] No hard-coded secrets (API keys, passwords, tokens, keys) in source code
- [ ] All secrets loaded via environment variables (`os.environ.get`, `process.env`, etc.)
- [ ] No `.env` files containing secrets in the repository
- [ ] No `secrets/` directory contents tracked by Git
- [ ] No private keys (`*.pem`, `*.key`) or certificates in the repository
- [ ] No model weights or training data files in the repository

## PHI Protection
- [ ] No patient names, IDs, MRNs, SSNs, DOBs, addresses, or phone numbers in:
    - Console output (`print`, `console.log`)
    - Application logs (any logging level)
    - Error messages or exception text
    - HTTP response bodies (including error responses)
    - Debug output or test output
- [ ] Any identifiers used in logs/tests are clearly synthetic (e.g., `SYNTH-*` prefix)
- [ ] Image file paths in logs or responses do not contain actual patient identifiers

## Test Data and Fixtures
- [ ] All test data uses synthetic identifiers:
    - Patient IDs start with `SYNTH-`
    - Medical record numbers are clearly fake
    - No real patient data or realistic facsimiles
- [ ] Test fixtures do not contain actual PHI

## Secrets Directory Protection
- [ ] The `secrets/` directory is listed in `.gitignore`
- [ ] Before writing to `secrets/`, verified that `.gitignore` includes `secrets/`
- [ ] No actual secrets stored in `secrets/` directory (use for non-sensitive configs only if at all)

## Configuration Safety
- [ ] Configuration files do not contain plain-text secrets
- [ ] Secrets in configs use environment variable substitution (e.g., `${VAR}` or `env.VAR`)
- [ ] TLS certificate paths are configured via environment variables, not hard-coded
- [ ] No connection strings with embedded credentials in config files

## Pre-commit Verification
- [ ] Reviewed git diff for accidental secret inclusion
- [ ] Checked for strings that resemble keys/tokens (long alphanumeric strings)
- [ ] Verified no patient-like identifiers appear in changed files
- [ ] Ran secret scanning tool if available (e.g., git-secrets, truffleHog)