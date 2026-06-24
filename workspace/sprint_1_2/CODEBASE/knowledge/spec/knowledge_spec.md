# Knowledge Stack Specification

## Purpose
Provides semantic and graph-based retrieval augmented generation (RAG) for clinical guideline explanations, evidence arbitration, and diagnostic reasoning using vector embeddings (Qdrant) and ontology relationships (ladybugDB) with LLM grounding.

## Owner
Knowledge Engineering Team

## Boundary
Qdrant vector database instances, ladybugDB graph database instances, embedding model servers, LLM inference endpoints, knowledge curation pipelines, and validation/verification workflows.

## Internal Design
- Hybrid knowledge architecture: vector similarity search + graph traversal
- pgVec: stores guideline section embeddings (BioClinicalBERT, PubMedBERT) with payload metadata
- ladybugDB: stores ontology concepts (SNOMED-CT, LOINC, RadLex) and relational axioms
- EmbeddingGemma: generates 768-dimension vectors for text chunks
- GemmaE2B/MedGemma: LLM for answer generation with constrained decoding
- Retrieval pipeline: hybrid search (vector + BM25) → graph expansion → reranking
- Grounding module: verifies LLM outputs against source guidelines with citation extraction
- Arbitration engine: resolves conflicting evidence using belief propagation
- Continuous integration: automated guideline ingestion from trusted sources (NIH, CDC, radiology societies)
- Versioned knowledge bases with temporal validity tracking
- Monitoring: retrieval relevance, grounding accuracy, latency SLOs

## Interface Contract
See `bento/knowledge/spec/interface-contract.md`.

## Consumers
- frontend:guideline-spec (for displaying grounded explanations in UI)
- backend:api-spec (for analysis explanation generation)
- ml:engine-spec (for generating model activation explanations)

## Breaking-change Policy
- Knowledge schema versioning via semantic versioning
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