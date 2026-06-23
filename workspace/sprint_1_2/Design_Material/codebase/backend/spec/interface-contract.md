# Backend Interface Contract

## Purpose
Orchestrates API routers, role checks, Socratic circuit-breaker state evaluations, and coordinates ML inference, telemetry collection, and data persistence.

## Owner
Core Backend Team

## Provides
- api endpoints (session management, frame upload, analysis jobs, reporting, feedback, safety endpoints)
- model inference orchestration (dispatches to Triton, aggregates results)
- telemetry collection (edge-based behavioral summaries, audit logs)
- data persistence coordination (writes to Postgres, S3, Redis)

## Consumes
- data:storage-spec (Postgres DB, S3 object store, Redis cache)
- ml:inference-spec (Triton server for angle, inflammation, segmentation, severity)
- knowledge:guideline-spec (Qdrant vector DB, ladybugDB graph DB for grounded explanations)

## Consumers
- frontend

## Not Directly Consumable
- data internals (Postgres tables, S3 object layout, Redis keys)
- ml internals (Triton model details, GPU kernels)
- knowledge internals (Qdrant vectors, ladybugDB graph)

## Breaking-change Policy
- API versioning via path (e.g., /api/v1/).
- Backward compatibility maintained for one minor version.
- Deprecation notices issued in release notes.
- Model interface changes (input/output tensors) require version bump.

## References
- NFR-7 (Real-Time UI Screen Refresh ≤200ms)
- NFR-10 (Generative Safety Guardrails)
- NFR-11 (Frontline Usability & Training)
- UC-48376 (Load Patient Scan Session)
- UC-47988 (Review Suggested Synovitis Grade)
- UC-25776 (Generate GradCAM & CoT Explanation Panel)
- UC-02423 (Log High-Trust Concur Block)
- UC_Q2_* (All Quadrant 2 safety workflows)
- UC_Q3_* (All Quadrant 3 subservience workflows)
- UC_Q4_* (All Quadrant 4 double-blind workflows)
- SOFTWARE_SYSTEM_DESIGN_FR_25.md (Sections 1.2, 2.1-2.6)
- SOLUTION_ARCHITECTURE_SPEC.md (Sections 2.1-2.6)
