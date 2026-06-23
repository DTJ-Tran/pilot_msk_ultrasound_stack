# Checklist: design_pattern_compliance

## Layered Architecture (Backend)
- [ ] No direct calls from presentation layer to data access layer
- [ ] Controllers only handle HTTP concerns (validation, serialization, routing)
- [ ] Business logic resides in service layer
- [ ] Data access layer handles only persistence concerns
- [ ] No upward dependencies (data layer does not depend on service layer)

## Dependency Injection
- [ ] No direct instantiation of infrastructure dependencies (e.g., `new MongoClient()`)
- [ ] Dependencies are injected (constructor, setter, or framework DI)
- [ ] Classes depend on interfaces/protocols, not concrete implementations
- [ ] Framework-appropriate DI mechanisms are used (e.g., FastAPI Depends, Spring @Autowired)

## Interface-Driven Development
- [ ] Business logic depends on abstractions (interfaces/repositories)
- [ ] No direct infrastructure calls in business logic (no `boto3`, `psycopg2.connect()`, etc. in services)
- [ ] Concrete implementations exist for interfaces but are injected, not instantiated internally

## Frontend State Management (Zustand)
- [ ] Global shared state is managed in Zustand stores
- [ ] Component state (`useState`) is used only for:
    - Form inputs and UI controls
    - Temporary UI state (loading states for local effects, animation states)
    - Data that is truly isolated to a single component
- [ ] Store follows naming convention: `use[Domain]Store`
- [ ] Store actions are named as verbs
- [ ] No business logic in components that should be in store actions

## Infrastructure as Code
- [ ] Terraform configuration uses a remote backend (GCS, S3, etc.)
- [ ] No local `terraform.tfstate` files committed
- [ ] Resources are named with environment identifier (e.g., `${var.environment}`)
- [ ] IAM roles follow least privilege principle (specific permissions, no wildcards)
- [ ] Separate configurations or workspaces for different environments
- [ ] All providers and modules have explicit version pins
- [ ] Terraform files are formatted (`terraform fmt`)

## Dependency Pinning
- [ ] Python: `requirements.txt` or `pyproject.toml` contains exact versions (no `~`, `>`, `<` without corresponding lock file)
- [ ] Python: If using `pyproject.toml` with poetry or pipenv, lock file (`poetry.lock` or `Pipfile.lock`) is present
- [ ] Node.js: `package-lock.json` or `yarn.lock` is present and matches `package.json`
- [ ] Other languages: Equivalent lock files are present and committed
- [ ] No unpinned dependencies that could cause non-reproducible builds

## Code Quality
- [ ] Duplicated code has been considered for extraction
- [ ] Preference given to composition over inheritance where applicable
- [ ] Utility functions are placed in appropriate shared locations
- [ ] No "God classes" or objects with too many responsibilities