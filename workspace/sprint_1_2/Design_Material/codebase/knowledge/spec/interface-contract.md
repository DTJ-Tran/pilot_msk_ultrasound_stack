# Knowledge Stack Interface Contract

## Purpose
Provides semantic and graph-based retrieval augmented generation (RAG) for clinical guideline explanations, evidence arbitration, and diagnostic reasoning using vector embeddings (Qdrant) and ontology relationships (ladybugDB) with LLM grounding.

## Owner
Knowledge Engineering Team

## Provides
- guideline embeddings and vector similarity search (Qdrant)
- ontology relationships and graph traversal (ladybugDB)
- grounded explanation generation (retrieval + LLM + grounding)
- evidence arbitration and belief propagation for conflicting evidence
- knowledge versioning and temporal validity tracking
- hallucination detection and policy enforcement

## Consumes
- (none) – Knowledge stack provides foundational AI services; it does not consume other rooms' interfaces for its core purpose.
  Note: Knowledge consumes internal storage (Qdrant, ladybugDB) and embedding/LLM services which are part of its boundary.

## Consumers
- frontend: consumes grounded explanations for UI display via `frontend:guideline-spec`.
- backend: consumes explanation generation for analysis reporting via `backend:api-spec`.
- ml: consumes model activation explanations via `ml:engine-spec`.

## Not Directly Consumable
- internal Qdrant collection names, vector dimensions, and indexing parameters
- ladybugDB schema details (predicate names, ontology version)
- embedding model specifics (model ID, tensor shapes)
- LLM prompt templates and decoding parameters
- knowledge curation pipeline details (source ingestion, validation)

## Breaking-change Policy
- Knowledge schema versioning via semantic versioning (MAJOR.MINOR.PATCH)
- Embedding model changes: require MAJOR version if dimension or architecture changes
- Ontology updates: backward compatible additions (MINOR), breaking changes require MAJOR
- LLM interface changes: versioned endpoints with deprecation windows
- Knowledge consumers must validate compatibility with new versions
- Deprecation notices for breaking changes 60 days in advance
- Automated migration tools for knowledge base version upgrades

## References
- NFR-3 (Explanation Latency ≤2s @ 95th percentile)
- NFR-6 (Guideline Coverage ≥95% of common synovitis queries)
- NFR-10 (Explanation Factuality Score ≥0.9)
- UC-25776 (Generate Grounded Explanation for Analysis)
- UC-65473 (Resolve Conflicting Evidence)
- SOLUTION_ARCHITECTURE_SPEC.md (Section 3.3)
- SOFTWARE_SYSTEM_DESIGN_FR_25.md (Section 4.3)
- GUIDELINE_SOURCES.md (Appendix B)
