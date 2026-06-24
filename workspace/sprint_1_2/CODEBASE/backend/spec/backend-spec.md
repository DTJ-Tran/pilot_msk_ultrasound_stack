# Backend Specification

## Purpose
Orchestrates API routers, role checks, Socratic circuit-breaker state evaluations, and coordinates ML inference, telemetry collection, and data persistence.

## Owner
Core Backend Team

## Boundary
FastAPI server, API routers, authentication middleware, circuit breaker engine, report generator, RAG coordinator, RAG-Referee (BERT), ledger logger, and connections to Postgres + pgvector, S3 (MinIO), Redis, Triton, ladybugDB.

## Internal Design
- Built with FastAPI (Python) and Uvicorn for async HTTP server.
- Authentication middleware validates JWT tokens and enforces RBAC (roles: RO_RADIOLOGIST, RO_THERAPIST).
- Socratic circuit-breaker engine monitors interaction telemetry (hover duration, decision time, override magnitude) and triggers safety dialogs.
- Clinical Report Engine uses ReportLab to generate bilingual PDF reports per Circular 46/2018/TT-BYT.
- RAG Coordinator orchestrates Retrieval-Augmented Generation: dense vector lookup in pgvector (PostgreSQL HNSW), graph traversal in ladybugDB, mandatory pre-generation retrieval, prompt enrichment, LLM generation on browser WebLLM (GemmaE2B) or cloud Vertex AI (MedGemma via NFR-16a), and hallucination guarding via BERT RAG-Referee.
- NLP Scrubber (Microsoft Presidio): re-verifies client edge redaction, refines residual PII, and returns error if unresolvable.
- Ledger Logger appends immutable, cryptographically chained audit logs to Postgres via triggers preventing UPDATE/DELETE.
- Connections: Postgres + pgvector (via SQLAlchemy), S3 (via boto3), Redis (via redis-py), Triton (via gRPC — CV + EmbeddingGemma only), ladybugDB (via in-process C++ bindings).
- Model weights loaded at startup from internal registry; cached in memory.
- API endpoints layered: public clinical (sessions, analysis, reports, feedback) and internal/local safety (explanations, safety, drift, RAG, activations, annotations, ground-truth, escalation, morphology, telemetry).

## Interface Contract
See `bento/backend/spec/interface-contract.md`.

## Consumers
- frontend

## Breaking-change Policy
See `bento/backend/spec/interface-contract.md`.

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
- DATA_ENGINEERING_SPEC.md (Sections 4-12 for domain objects)
- CI_CD_DEPLOYMENT_PIPELINE.md (Section 9.2 for docker-compose)
