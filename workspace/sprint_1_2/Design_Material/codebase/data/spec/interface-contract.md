# Data Model Interface Contract

## Purpose
Manages persistent storage, caching, and object storage for clinical data including patient records, imaging studies, analysis results, and audit trails using PostgreSQL, Redis, and S3 with calibration services.

## Owner
Data / Domain Team

## Provides
- persistent-storage (ACID-compliant patient/study/session records)
- object-storage (binary imagery, masks, overlays, exported reports)
- caching-layer (session state, rate limiting counters, temp computation results)
- calibration-service (pixel-to-mm conversion factors per device/protocol)
- backup-and-recovery (point-in-time recovery, cross-region replication)
- data-export-functionality (DICOM, PDF, CSV formats)

## Consumes
- (None - foundational storage layer)

## Consumers
- backend:api-spec (patient/study/session CRUD operations, search)
- backend:ledger-spec (audit trail append-only storage)
- ml:engine-spec (model artifacts storage/retrieval, training datasets)
- knowledge:spec (guideline documents, vectorization source material)
- infra:spec (shared PostgreSQL/Redis instances for platform services)

## Not Directly Consumable
- internal table structures beyond published schemas
- connection pool tuning parameters
- Redis key naming conventions for internal caching
- S3 bucket policies beyond published access patterns
- backup encryption key management
- vacuum/analyze maintenance schedules

## Breaking-change Policy
- Database schema versioning via semantic versioning (MAJOR.MINOR.PATCH aligned with API)
- Additive changes (new tables/columns): backward compatible (MINOR version)
- Breaking changes (removed columns, type alterations): require MAJOR version
- Migration scripts provided for all breaking changes with rollback procedures
- Deprecation notices for schema changes issued 90 days in advance
- Storage interface changes (S3 prefixes, Redis keys) follow same versioning
- Consumers must opt-in to breaking changes via feature flags

## References
- NFR-7 (Data Durability: 99.999999999% annual)
- NFR-8 (Recovery Time Objective ≤4 hours)
- NFR-9 (Storage Cost Efficiency)
- NFR-13 (Audit Trail Immutability)
- UC-48376 (Load Patient Scan Session)
- UC-92006 (Save Analysis Results)
- UC-01580 (Export Study Package)