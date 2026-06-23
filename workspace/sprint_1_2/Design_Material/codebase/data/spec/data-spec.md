# Data Model Specification

## Purpose
Manages persistent storage, caching, and object storage for clinical data including patient records, imaging studies, analysis results, and audit trails using PostgreSQL, Redis, and S3 with calibration services.

## Owner
Data / Domain Team

## Boundary
PostgreSQL database clusters, Redis cache instances, S3 buckets/object storage, database connection pools, cache invalidation strategies, and storage lifecycle management policies.

## Internal Design
- PostgreSQL 15 with TimescaleDB extension for temporal data
- Schema organization: patient, study, session, analysis, audit, calibration namespaces
- Connection pooling via PgBouncer for efficient database access
- Redis 7 for session caching, rate limiting, and temporary computation results
- S3 bucket structure: raw-imagery, processed-results, exports, backups with lifecycle policies
- Encryption-at-rest for sensitive data (PHI) using AES-256-GCM
- Automated backups with point-in-time recovery (PITR) capabilities
- Read replicas for query distribution and reporting workloads
- Calibration service: pixel-to-mm conversion factors stored per device/protocol
- Data retention policies: active data (2 years), archived data (7 years), purged data (>7 years)
- Migration system using Flyway for schema versioning
- Monitoring: query performance, connection pool utilization, replication lag

## Interface Contract
See `bento/data/spec/interface-contract.md`.

## Consumers
- backend:api-spec (for CRUD operations on patient/study/session data)
- backend:ledger-spec (for audit trail storage)
- ml:engine-spec (for model weights and training data)
- knowledge:spec (for exporting vectorizable content)

## Breaking-change Policy
- Database schema versioning via semantic versioning aligned with API versions
- Table/column additions: backward compatible (MINOR version)
- Table/column removals or type changes: require MAJOR version with migration path
- API contract changes follow backend interface contract policies
- Data migration scripts provided for breaking changes
- Deprecation notices for schema changes 60 days in advance

## References
- NFR-7 (Data Durability: 99.999999999% annual)
- NFR-8 (Recovery Time Objective ≤4 hours)
- NFR-9 (Storage Cost Efficiency)
- NFR-13 (Audit Trail Immutability)
- UC-48376 (Load Patient Scan Session)
- UC-92006 (Save Analysis Results)
- UC-01580 (Export Study Package)
- SOLUTION_ARCHITECTURE_SPEC.md (Section 2.3)
- SOFTWARE_SYSTEM_DESIGN_FR_25.md (Section 5.2)