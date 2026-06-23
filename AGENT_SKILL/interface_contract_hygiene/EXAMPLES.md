# Examples: interface_contract_hygiene

## Correct Examples

### Backend Service Contract Example
File: `backend/services/patient_service/spec/interface_contract.md`

```markdown
# Patient Service Interface Contract

## Purpose
Handles all patient-related business operations including registration, updates, and retrieval of patient records. Provides a clean API for frontend and other backend services.

## Owner
Platform Team (platform-team@vkist.example.com)

## Boundary
**Includes:**
- Patient data validation
- Appointment scheduling logic
- Insurance verification workflows
- HL7 message parsing for patient demographics

**Excludes:**
- Image storage and retrieval (handled by Imaging Service)
- Payment processing (handled by Billing Service)
- User authentication (handled by Auth Service)

## Breaking-change Policy
- **MINOR version**: Adding new optional fields to patient schema, new endpoints for non-core features
- **MAJOR version**: Removing fields, changing data types of existing fields, removing endpoints
  - Requires 60-day deprecation period
  - Migration guide provided in release notes
  - Deprecation warnings added 30 days prior to removal

## Consumers
- Frontend Patient Portal (`frontend/modules/patient_portal`)
- Appointment Scheduling Service (`backend/services/scheduling`)
- Billing Service (`backend/services/billing`)
- Mobile App API (`backend/services/mobile-api`)

## References
- [Patient Data Model](../models/patient_model.md)
- [API Specification](api-spec.yaml)
- [HL7 Interface Specification](../integrations/hl7-spec.md)
```

### Frontend Module Contract Example
File: `frontend/modules/appointment_scheduler/spec/interface_contract.md`

```markdown
# Appointment Scheduler Module Contract

## Purpose
Provides UI components and state management for scheduling, rescheduling, and cancelling patient appointments. Integrates with calendar services and sends notifications.

## Owner
Frontend Team (frontend-team@vkist.example.com)

## Boundary
**Includes:**
- Appointment booking form components
- Calendar view widgets
- Conflict detection logic
- Notification scheduling (email/SMS)
- Form validation for appointment constraints

**Excludes:**
- Patient identity verification (handled by Auth Module)
- Payment collection for appointments (handled by Billing Module)
- Actual calendar sync with external systems (handled by Calendar Integration Service)

## Breaking-change Policy
- **MINOR**: Adding new optional props to components, new utility functions
- **MAJOR**: Removing props, changing prop types, removing components
  - Requires minor version bump in package.json
  - Migration guide in CHANGELOG.md
  - Deprecated props logged as warnings for 2 minor versions

## Consumers
- Main App Layout (`frontend/layout/MainLayout`)
- Patient Dashboard (`frontend/modules/patient_dashboard`)
- Provider Portal (`frontend/modules/provider_portal`)

## References
- [Component Library Guidelines](../../shared/components/README.md)
- [API Contract with Backend](../services/appointment_service/spec/interface-contract.md)
- [Accessibility Requirements](../../docs/accessibility.md)
```

### Infrastructure Module Contract Example
File: `infra/modules/networking/spec/interface_contract.md`

```markdown
# Networking Module Contract

## Purpose
Defines AWS/VPC networking infrastructure including subnets, route tables, security groups, and DNS configuration for the VKIST deployment.

## Owner
Infrastructure Team (infra-team@vkist.example.com)

## Boundary
**Includes:**
- VPC creation and CIDR allocation
- Public and private subnet configuration
- Internet gateway and NAT gateway setup
- Route table association
- Security group baseline rules
- DNS zone and record creation

**Excludes:**
- Compute resources (EC2/EKS) (handled by compute modules)
- Database infrastructure (handled by database module)
- Application-level security (handled by respective service modules)

## Breaking-change Policy
- **MINOR**: Adding new subnets, adding non-restrictive security group rules
- **MAJOR**: Changing VPC CIDR, removing subnets, altering route tables that break connectivity
  - Requires terraform state migration plan
  - 30-day review period with stakeholders
  - Backward compatibility maintained via Terraform state import where possible

## Consumers
- Compute Module (`infra/modules/compute`)
- Database Module (`infra/modules/database`)
- EKS Cluster Module (`infra/modules/eks`)
- All environment-specific configurations (staging, production)

## References
- [AWS VPC Best Practices](../docs/aws_vpc_best practices.md)
- [Network Security Policy](../../docs/security/network_policy.md)
- [Terraform Module Guidelines](../../modules/README.md)
```

## Incorrect Examples (to avoid)

### Missing Contract
```diff
- // No spec/interface-contract.md exists for this new service
+ mkdir -p backend/services/new_service
+ touch backend/services/new_service/main.py
```

### Incomplete Contract
```markdown
# Incomplete Service
## Purpose
Handles user notifications.

// Missing: Owner, Boundary, Breaking-change Policy, Consumers, References
```

### Wrong Location
```diff
- // Contract should be in spec/ but is placed in root
+ NEW SERVICE/
+   interface_contract.md   // WRONG LOCATION
+   main.py
+   requirements.txt
```