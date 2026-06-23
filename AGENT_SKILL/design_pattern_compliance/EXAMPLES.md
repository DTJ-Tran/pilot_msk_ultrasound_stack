# Examples: design_pattern_compliance

## Correct Examples

### Layered Architecture (Python/FastAPI)
```python
# GOOD: Proper layer separation
# presentation layer (api/patients.py)
from fastapi import APIRouter, Depends, HTTPException
from services.patient_service import PatientService
from models.patient import PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])

def get_patient_service() -> PatientService:
    # Dependency injection - could come from a DI container
    return PatientService(
        repository=PatientRepository()  # In practice, this would be injected
    )

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: str,
    service: PatientService = Depends(get_patient_service)
):
    """Controller handles only HTTP concerns."""
    patient = service.get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# service layer (services/patient_service.py)
from repositories.patient_repository import PatientRepository
from models.patient import PatientModel

class PatientService:
    def __init__(self, repository: PatientRepository):
        self.repository = repository  # Dependency injected
    
    def get_patient_by_id(self, patient_id: str) -> Optional[PatientModel]:
        # Business logic lives here
        return self.repository.get_by_id(patient_id)


# data access layer (repositories/patient_repository.py)
from models.patient import PatientModel

class PatientRepository:
    def get_by_id(self, patient_id: str) -> Optional[PatientModel]:
        # Data access concerns only
        # In real implementation, this would query a database
        pass
```

### Dependency Injection with Interfaces
```python
# GOOD: Interface-based dependencies
from abc import ABC, abstractmethod
from typing import Protocol

# Define interface (protocol)
class PatientRepository(Protocol):
    def get_by_id(self, patient_id: str) -> Optional[PatientModel]: ...
    def save(self, patient: PatientModel) -> bool: ...

# Concrete implementation
class PostgreSQLPatientRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def get_by_id(self, patient_id: str) -> Optional[PatientModel]:
        # Implementation details
        pass

# Service depends on interface, not concrete class
class PatientService:
    def __init__(self, repository: PatientRepository):  # Accepts any implementation
        self.repository = repository
    
    def get_patient(self, patient_id: str) -> Optional[PatientModel]:
        return self.repository.get_by_id(patient_id)

# Usage with dependency injection
def get_patient_service() -> PatientService:
    repo = PostgreSQLPatientRepository(os.getenv("DB_CONNECTION"))
    return PatientService(repository)
```

### Frontend Zustand Store
```javascript
// GOOD: Proper Zustand store usage
import { create } from 'zustand';

// Patient store slice
const usePatientStore = create((set, get) => ({
  // State
  patients: [],
  loading: false,
  error: null,
  
  // Actions
  setPatients: (patients) => set({ patients }),
  fetchPatients: async () => {
    set({ loading: true, error: null });
    try {
      const response = await api.getPatients();
      set({ patients: response.data, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },
  addPatient: (patient) => set((state) => ({
    patients: [...state.patients, patient],
    loading: false,
    error: null
  })),
}));

// Component using store - ONLY for UI state
import { useState } from 'react';
import { usePatientStore } from '../store/patientStore';

export const PatientForm: React.FC = () => {
  // LOCAL UI state only - correct use of useState
  const [name, setName] = useState('');
  const [dob, setDob] = useState('');
  const [submitting, setSubmitting] = useState(false);
  
  // GLOBAL state from store
  const { patients, loading, error, addPatient } = usePatientStore();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await addPatient({ id: Date.now(), name, dob });
      setName('');
      setDob('');
    } finally {
      setSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields using local state */}
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
      <input value={dob} onChange={(e) => setDob(e.target.value)} placeholder="Date of Birth" />
      <button type="submit" disabled={submitting}>
        {submitting ? 'Adding...' : 'Add Patient'}
      </button>
      
      {/* Displaying global state */}
      {loading && <p>Saving...</p>}
      {error && <p>Error: {error}</p>}
    </form>
  );
};
```

### Infrastructure as Code (Terraform)
```hcl
# GOOD: Proper Terraform practices
terraform {
  # REQUIRED: Remote backend
  backend "gcs" {
    bucket = "vkist-terraform-state"
    prefix = "env/${var.environment}"
  }
  
  # REQUIRED: Versioned providers
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = ["dev", "staging", "prod"].contains(var.upper)
    error_message = "Environment must be either dev, staging, or prod."
  }
}

# RESOURCE NAMING with environment
resource "google_compute_instance" "vm" {
  name      = "vkist-${var.environment}-backend"
  machine_type = "e2-medium"
  
  # ... other configuration
}

# LEAST PRIVILEGE IAM
resource "google_service_account" "backend" {
  account_id   = "vkist-backend-${var.environment}"
  display_name = "VKIST Backend Service Account"
}

# Grant only necessary roles
resource "google_project_iam_member" "storage_reader" {
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.backend.email}"
}

# VERSIONED MODULES
module "network" {
  source  = "terraform-google-modules/network/google"
  version = "~> 5.0"
  
  project_id   = var.project_id
  network_name = "vkist-${var.environment}-net"
  # ... other parameters
}
```

### Dependency Pinning
```txt
# GOOD: requirements.txt with exact versions
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.1
python-multipart==0.0.6
```

```json
// GOOD: package.json with package-lock.json
{
  "name": "vkist-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "zustand": "^4.4.1",
    "axios": "^1.6.2"
  }
}
// package-lock.json ensures exact versions are installed
```

## Incorrect Examples (to avoid)

### Layer Violation
```python
# BAD: Controller directly accessing repository (skipping service layer)
from fastapi import APIRouter, Depends
from repositories.patient_repository import PatientRepository

router = APIRouter()

@router.get("/patients/{id}")
def get_patient(patient_id: str, repo: PatientRepository = Depends()):
    # VIOLATION: Presentation layer accessing data layer directly
    return repo.get_by_id(patient_id)
```

### Direct Infrastructure Instantiation
```python
# BAD: Service creating its own database connection
import psycopg2
import os

class PatientService:
    def __init__(self):
        # VIOLATION: Direct instantiation of infrastructure
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    
    def get_patient(self, patient_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        return cursor.fetchone()
```

### Frontend Anti-pattern: State in Components
```javascript
// BAD: Using useState for shared data that should be in store
import { useState, useEffect } from 'react';
import { fetchPatients } from '../api/patientApi';

export const PatientList: React.FC = () => {
  // WRONG: This state is shared and should be in a store
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    const loadPatients = async () => {
      setLoading(true);
      try {
        const data = await fetchPatients();
        setPatients(data); // This state might be needed by other components
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    
    loadPatients();
  }, []);
  
  // ... render logic
};

// If another component needs patients data, it would have to fetch again
// or receive it via props - inefficient and not scalable
```

### Infrastructure Mistakes
```hcl
# BAD: Local state storage (should be remote)
terraform {
  # MISSING: backend configuration
  # state will be stored locally - VIOLATION
}

# BAD: Hard-coded environment (should be variable)
resource "google_compute_network" "vpc" {
  name = "vkist-prod-network"  # What if we want to deploy to staging?
}

# BAD: Overly permissive IAM
resource "google_project_iam_member" "admin" {
  role   = "roles/editor"  # Too permissive - VIOLATION of least privilege
  member = "user:admin@example.com"
}

# BAD: Unpinned module version
module "network" {
  source = "terraform-google-modules/network/google"
  # MISSING: version parameter - could get breaking changes on next run
}
```

### Dependency Issues
```txt
# BAD: Unpinned dependencies in requirements.txt
fastapi
uvicorn
pydantic
# Any of these could break on next pip install
```

```json
// BAD: Missing or outdated lock file
{
  "name": "my-app",
  "dependencies": {
    "lodash": "^4.17.21"
    // No package-lock.json - versions not locked
  }
}
```