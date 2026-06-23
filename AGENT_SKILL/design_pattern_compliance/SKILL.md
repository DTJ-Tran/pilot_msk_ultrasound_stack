# Skill: design_pattern_compliance

## Trigger Conditions
- Creation of a new class, function, or module
- Significant refactoring of existing code (architectural changes)
- Adding new infrastructure (Terraform modules)
- Creating new state slices
)

## Rules

### 1. Layered Architecture (Backend)
- **Direction of Dependencies**: 
    - Presentation layer (API controllers) → Service layer → Data Access layer
    - No skipping layers (e.g., controller directly accessing repository)
    - No upward dependencies (data layer should not depend on service layer)
- **Separation of Concerns**:
    - Controllers handle HTTP concerns only (validation, serialization, routing)
    - Services contain business logic and orchestration
    - Data Access/Repositories handle persistence concerns only
- Severity: `[ERROR]`

### 2. Dependency Injection and Inversion of Control
- **No Direct Instantiation**: 
    - Classes should not instantiate their dependencies directly (especially infrastructure clients)
    - Dependencies should be injected via constructor or setter
- **Interface-Based Dependencies**:
    - Depend on abstractions (interfaces/protocols) rather than concrete implementations
    - Example: Service depends on `DatabaseRepository` interface, not `PostgreSQLRepository` directly
- **Framework-Compatible DI**:
    - Use framework-provided dependency injection (e.g., FastAPI's `Depends`, Spring `@Autowired`)
    - Avoid service locator pattern
- Severity: `[ERROR]`

### 3. Interface-Driven Development
- **Program to Interfaces**:
    - Concrete classes should implement defined interfaces
    - Clients should depend on interfaces, not implementations
- **No Concrete Infra in Business Logic**:
    - Business logic should not contain direct calls to infrastructure (e.g., `boto3.client()`, `psycopg2.connect()`)
    - Infrastructure access should be abstracted behind repository/service interfaces
- Severity: `[ERROR]`

### 4. Frontend State Management (Zustand)
- **Store Slices**:
    - Global state should be split into logical slices using Zustand
    - Each slice corresponds to a domain (e.g., `usePatientStore`, `useAppointmentStore`)
- **No Inline State for Shared Data**:
    - Component state (`useState`) should only be used for:
        - UI-specific state (form inputs, toggles, animation states)
        - Data that is not shared across components
    - Any data that is shared across components or needed by multiple hooks should be in a store
- **Store Structure**:
    - Follow consistent naming: `use[Domain]Store`
    - Actions should be named as verbs (e.g., `setPatients`, `fetchAppointments`)
    - Selectors should be derived and memoized where appropriate
- Severity: `[ERROR]`

### 5. Infrastructure as Code (IaC) Best Practices
- **Terraform State**:
    - All Terraform configurations must use a remote backend (GCS recommended for this project)
    - No local `terraform.tfstate` files in the repository
- **Resource Naming**:
    - Use consistent naming conventions that include environment (e.g., `vkist-${var.environment}-service`)
- **Least Privilege IAM**:
    - IAM roles and policies must grant only the permissions necessary
    - Avoid using wildcard permissions (`*`) or overly broad roles
- **Environment Separation**:
    - Use separate workspaces or directories for different environments (e.g., `env/staging`, `env/prod`)
    - Do not use the same resources for different environments
- **Version Pinning**:
    - All external dependencies must be version-pinned:
        - Terraform modules: `source = "terraform-google-modules/network/google//version"`
        - Provider versions explicitly set
- Severity: `[ERROR]`

### 6. Dependency Pinning
- **Python**:
    - `requirements.txt` or `pyproject.toml` must contain exact versions (no wildcards)
    - Use `pip freeze > requirements.txt` for deterministic builds
- **Node.js**:
    - `package-lock.json` or `yarn.lock` must be committed and up to date
    - Dependencies in `package.json` should use caret (`^`) or tilde (`~`) ranges appropriately, but lock file ensures reproducibility
- **Other Ecosystems**:
    - Equivalent lock files must be present and committed (e.g., `Pipfile.lock`, `poetry.lock`, `Cargo.lock`)
- Severity: `[ERROR]`

### 7. Code Reusability and Abstraction
- **Avoid Duplication**:
    - Similar code in two or more places should be extracted to a shared utility or component
- **Prefer Composition Over Inheritance**:
    - Especially in complex domain models, favor composing behavior over deep inheritance hierarchies
- **Utility Functions**:
    - Place truly generic utilities in shared locations (e.g., `utils/`, `lib/`)
    - Avoid creating utility classes with only static methods if not needed in the language
- Severity: `[WARN]`