# Examples: secrets_and_phi_safety

## Correct Examples

### Secret Loading
```python
# Good: Loading from environment variables
import os

API_KEY = os.environ.get("EXTERNAL_API_KEY")
if not API_KEY:
    raise ValueError("EXTERNAL_API_KEY environment variable not set")

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-key-change-in-prod")
```

```javascript
// Good: Node.js environment variables
const apiKey = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;

if (!apiKey || !dbPassword) {
  throw new Error('Missing required environment variables');
}
```

### PHI Protection in Logs
```python
# Good: Logging without PHI
import logging
import hashlib

logger = logging.getLogger(__name__)

def process_patient_record(patient_record):
    # Log only non-identifying information
    logger.info(
        f"Processing record for patient age group: {get_age_group(patient_record.age)}"
    )
    
    # If logging an ID is absolutely necessary, use a hash
    patient_hash = hashlib.sha256(
        patient_record.medical_record_number.encode()
    ).hexdigest()[:8]
    logger.debug(f"Processing hashed MRN: {patient_hash}...")
    
    # Never do this:
    # logger.info(f"Processing patient {patient_record.name} (MRN: {patient_record.mrn})")
    # logger.error(f"Failed to process {patient_record.id}: {str(e)}")  # if id is PHI
```

### Test Data with Synthetic Identifiers
```python
# Good: Test fixtures use SYNTH-* prefix
TEST_PATIENTS = [
    {
        "patient_id": "SYNTH-PAT-0001",
        "name": "John Doe",  # Note: In real tests, even names should be fake/synthetic
        "mrn": "SYNTH-MRN-0001",
        "date_of_birth": "1980-01-01",
        # ... other test fields
    },
    {
        "patient_id": "SYNTH-PAT-0002",
        "name": "Jane Smith",
        "mrn": "SYNTH-MRN-0002",
        "date_of_birth": "1992-05-15",
    }
]
```

### Configuration Files
```yaml
# Good: docker-compose.yml using environment variables
version: '3.8'
services:
  api:
    image: medical-api:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    secrets:
      - db_cert  # Reference to external secret store, not file in repo

# Secrets are NOT stored in the repo
# Use Docker secrets or Kubernetes secrets or similar external secret management
```

```ini
# Good: config.ini with environment variable substitution
[database]
url = ${DATABASE_URL}
# or using os.path.expandvars equivalent
```

### .gitignore Protection
```gitignore
# .gitignore at repository root
# ... other entries
secrets/
*.env
*.pem
*.key
```

### Safe Error Messages
```python
# Good: Generic error messages that don't leak PHI
try:
    process_claim(claim_data)
except ValidationError as e:
    # Log detailed error internally (without PHI)
    logger.warning(f"Claim validation failed: {e}")
    # Return generic message to user
    raise HTTPException(
        status_code=400,
        detail="Claim validation failed. Please check the submitted information."
    )
except Exception as e:
    logger.error(f"Unexpected error processing claim: {e}")
    raise HTTPException(
        status_code=500,
        detail="Internal server error. Please contact support."
    )
```

## Incorrect Examples

### Secret Exposure
```python
# Bad: Hard-coded secret
API_KEY = "sk_live_1234567890abcdef"  # VIOLATION: exposed in code

# Bad: Secret in config file committed to repo
# config.yaml
# api_key: "actual_secret_key_here"  # VIOLATION

# Bad: Using .env file that gets committed
# .env (committed to git)
# DATABASE_URL=postgres://user:password@localhost/db
```

### PHI in Logs and Errors
```python
# Bad: Logging full patient identifier
logger.error(f"Failed to update patient {patient.patient_id}: {str(e)}")
# If patient_id is MRN or similar, this leaks PHI

# Bad: Error message with PHI
raise ValueError(f"Invalid DOB for patient {patient.name}: {patient.dob}")

# Bad: Including PHI in HTTP response
return {
    "error": f"Patient {patient.mrn} not found",  # MRN is PHI
    "code": "PATIENT_NOT_FOUND"
}
```

### Real Data in Tests
```python
# Bad: Test using real patient-like data
TEST_PATIENT = {
    "patient_id": "12345678",  # Looks like real MRN
    "name": "John Doe",        # Realistic name
    "ssn": "123-45-6789",      # Actual SSN format
    "dob": "1980-01-01",
}
```

### Missing .gitignore Protection
```gitignore
# .gitmissing: secrets/ directory NOT ignored
# This would allow secrets to be committed
# (no entry for secrets/ here)
```

### Insecure Configuration
```yaml
# Bad: Hard-coded secrets in config
database:
  host: localhost
  port: 5432
  username: admin
  password: "super_secret_password"  # VIOLATION

tls:
  cert_file: "/etc/ssl/certs/real-cert.pem"  # Hard-coded path, should be env var
  key_file: "/etc/ssl/private/real-key.pem"
```