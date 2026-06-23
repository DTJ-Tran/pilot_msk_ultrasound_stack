# Examples: file_naming_convention

## Correct Examples

### File Naming
- `patient_data.csv` → ❌ (forbidden extension, should be external)
- `patient_data.json` → ✅ (allowed extension, snake_case)
- `Dockerfile` → ✅ (UPPER_SNAKE_CASE allowed for root config)
- `docker-compose.yaml` → ✅ (hyphen allowed exception)
- `docker-compose.yml` → ✅ (hyphen allowed exception)
- `package-lock.json` → ✅ (hyphen allowed exception)
- `yarn.lock` → ✅ (hyphen allowed exception)
- `pnpm-lock.yaml` → ✅ (hyphen allowed exception)
- `config.json` → ✅ (snake_case, allowed extension)
- `api/v1/patient_routes.py` → ✅ (snake_case in path)

### Directory Naming
- `data_models/` → ✅
- `api_v2/` → ✅
- `legacy_data/` → ✅ (but see LEGACY/ rule below)

### LEGACY/ Directory
```python
# LEGACY: Temporary fix for migration issue #123
# TODO: Remove after migration complete
legacy_code_here()
```
→ ✅ (includes required comment)

### Test Files
```
src/
  models/
    patient_model.py
tests/
  models/
    test_patient_model.py
```
→ ✅ (test file mirrors source path)

## Incorrect Examples

### File Naming
- `PatientData.json` → ❌ (PascalCase, should be snake_case)
- `patient-data.json` → ❌ (hyphen not allowed except docker-compose and lockfiles)
- `patient data.json` → ❌ (spaces not allowed)
- `patient.PDF` → ❌ (forbidden extension)
- `secret_key.pem` → ❌ (forbidden extension)
- `package_lock.json` → ❌ (should be package-lock.json with hyphens)
- `yarn_lock` → ❌ (should be yarn.lock with hyphen and extension)
- `docker_compose.yaml` → ❌ (should be docker-compose.yaml with hyphens)

### Directory Naming
- `DataModels/` → ❌ (PascalCase)
- `data-models/` → ❌ (hyphens not allowed)
- `data models/` → ❌ (spaces)

### LEGACY/ Directory
```python
# Modified legacy function
def old_function():
    pass
```
→ ❌ (missing `# LEGACY:` comment)

### Test Files
```
src/
  utils/
    helper.py
tests/
  test_helper.py  # ❌ Incorrect: should be tests/utils/test_helper.py
```
→ ❌ (test file does not mirror source path)