# Examples: coding_convention

## Correct Examples

### Python
```python
"""
Module: patient_service
Purpose: Handle patient-related business logic.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models.patient import PatientModel
from services.database import DatabaseService

router = APIRouter(prefix="/patients", tags=["patients"])


class PatientService:
    """Service for managing patient records.
    
    Attributes:
        db: Database service instance
    """
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def get_patient_by_id(self, patient_id: str) -> Optional[PatientModel]:
        """Retrieve a patient by their ID.
        
        Args:
            patient_id: Unique identifier for the patient
            
        Returns:
            PatientModel if found, None otherwise
            
        Side Effects:
            None
        """
        try:
            return self.db.get_patient(patient_id)
        except DatabaseError as e:
            logger.error(f"Failed to retrieve patient {patient_id}: {e}")
            raise
```

### TypeScript/React
```typescript
import { create } from 'zustand';
import { useEffect } from 'react';

// Hook name follows useSnakeCase
const usePatientStore = create<PatientState>((set, get) => ({
  patients: [],
  loading: false,
  error: null,
  
  fetchPatients: async () => {
    set({ loading: true, error: null });
    try {
      const response = await api.getPatients();
      set({ patients: response.data, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },
}));

export const PatientList: React.FC = () => {
  const { patients, loading, error } = usePatientStore();
  
  // Component name: PascalCase
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <ul>
      {patients.map(patient => (
        <li key={patient.id}>{patient.name}</li>
      ))}
    </ul>
  );
};
```

### Error Handling
```python
# Good: Using logging instead of print
import logging

logger = logging.getLogger(__name__)

def process_data(data: dict) -> dict:
    try:
        # Process data
        result = transform_data(data)
        return result
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        raise InvalidInputError(str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error in process_data: {e}")
        raise
```

### RBAC
```python
# Good: Using role constants
from auth.roles import RO_RADIOLOGIST, RO_THERAPIST

def can_read_patient_records(user_role: str) -> bool:
    return user_role in [RO_RADIOLOGIST, RO_THERAPIST]

# Bad: Hard-coded role strings
def can_read_patient_records_bad(user_role: str) -> bool:
    return user_role in ["radiologist", "therapist"]  # VIOLATION
```

### Configuration
```python
# Good: Loading from environment
import os

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
MAX_UPLOAD_SIZE = int(os.environ.get("MAX_UPLOAD_SIZE", "10485760"))  # 10MB

# Bad: Hard-coded values
API_BASE_URL = "http://localhost:8000"  # VIOLATION
```

### Commit Messages
```
feat(auth): add JWT refresh token endpoint
fix(patient-api): fix patient ID validation typo
docs(api): update patient endpoint documentation
refactor(core): extract database connection logic
```