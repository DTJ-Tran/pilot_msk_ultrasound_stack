# Frontend Interface Contract

## Purpose
Provides interactive clinical workspace, runs edge models (LiteRT, MediaPipe), handles client-side encryption (WebCrypto), offline sync via IndexedDB/Service Worker, and renders UI viewport with graphics adapter fallback.

## Owner
Web Experience Team

## Provides
- ui viewport (interactive canvas, overlays, controls)
- edge ml (angle classification, inflammation detection, ROI pre-cropping)
- offline sync (local cache, sync queue, background synchronization)

## Consumes
- backend:api-spec (REST API endpoints for session, analysis, reporting, feedback)
- knowledge:guideline-spec (GraphRAG pipeline for grounded explanations, evidence arbitration)

## Consumers
(None)

## Not Directly Consumable
- backend internals (e.g., FastAPI route implementations, Triton model details)
- knowledge internals (Qdrant vectors, ladybugDB graph structure)
- data internals (Postgres schema, S3 object layout)

## Breaking-change Policy
- API versioning via path (e.g., /api/v1/).
- Backward compatibility maintained for one minor version.
- Deprecation notices issued in release notes.
- Breaking changes require major version bump.

## References
- NFR-1 (Collaborative Rendering Speed ≤3s)
- NFR-4 (Client Memory Footprint ≤150MB)
- NFR-14 (Legacy Hardware Compatibility)
- UC-48376 (Load Patient Scan Session)
- UC-47988 (Review Suggested Synovitis Grade)
- UC-25637 (Expose Pixel-Level Activation Logic)
- UC-60739 (Isolate Visual Noise/Artifacts)
