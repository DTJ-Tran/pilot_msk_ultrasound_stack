# Skill: interface_contract_hygiene

## Trigger Conditions
- Creation of a new module, package, or component
- Any modification to a public API (function signatures, class interfaces, endpoints)
- Creation of a new directory that represents a logical boundary (e.g., new service, new frontend module)

## Rules

### 1. Interface Contract Requirement
- Every module boundary MUST have an `interface_contract.md` file in its `spec/` directory.
- Applies to: backend services, frontend modules, data access layers, infrastructure components.
- Severity: `[ERROR]`

### 2. Contract Content Requirements
Each `interface_contract.md` must include:
- **Purpose**: Brief description of what the module does
- **Owner**: Team or person responsible for the module
- **Boundary**: Clear definition of what is inside and outside the module
- **Breaking-change Policy**: How breaking changes are handled (versioning, deprecation)
- **Consumers**: List of other modules or systems that use this module
- **References**: Links to related documentation, diagrams, or external specifications
- Severity: `[ERROR]`

### 3. Versioning and Backward Compatibility
- Adding new fields, endpoints, or optional parameters: MINOR version bump (backward compatible)
- Removing or changing types of existing fields/endpoints: MAJOR version bump with:
  - Migration path documentation
  - 60-day deprecation notice minimum
  - Deprecation warnings in code
- Severity: `[ERROR]`

### 4. Template Consistency
- When creating a new `interface_contract.md`, the author MUST review existing contracts in the same domain for naming and template consistency.
- Use the same section headings and format as neighboring contracts.
- Severity: `[WARN]`

### 5. Contract Location
- Contract must be located at `<module_path>/spec/interface_contract.md`
- If `spec/` directory does not exist, it must be created.
- Severity: `[ERROR]`