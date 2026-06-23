# Checklist: interface_contract_hygiene

## New Module/Package Creation
- [ ] New module/package includes a `spec/` directory
- [ ] `spec/interface-contract.md` file exists in the new module
- [ ] Contract file is located at `<module_path>/spec/interface-contract.md`

## Contract Content Verification
- [ ] Contract includes a clear **Purpose** section
- [ ] Contract identifies an **Owner** (team or individual)
- [ ] Contract defines the **Boundary** (includes/excludes)
- [ ] Contract specifies a **Breaking-change Policy**
- [ ] Contract lists **Consumers** (other modules/systems that use this)
- [ ] Contract provides **References** to related documentation
- [ ] Contract follows the same format/structure as existing contracts in the same domain

## Contract Modification (Existing Modules)
When modifying a public API (changing function signatures, adding/removing endpoints, etc.):
- [ ] Breaking changes follow the versioning policy:
    - Adding features: MINOR version bump
    - Removing/changing types: MAJOR version with migration path and 60-day notice
- [ ] Deprecation warnings are added for removed/changed interfaces
- [ ] Migration documentation is provided for breaking changes

## Template Consistency Check
Before creating a new contract:
- [ ] Reviewed at least two existing interface-contract.md files in the same domain (backend/frontend/infra)
- [ ] Matched section headings and formatting conventions
- [ ] Used similar language and level of detail