# Offline Specification

## Purpose
Provides offline caching and synchronization for the PWA frontend, enabling continued operation during network interruptions and seamless sync upon reconnection.

## Owner
Web Experience Team (same as frontend)

## Parent
frontend

Boundary
IndexedDB database via Dexie.js, Service Worker for background sync, and local queue for offline actions.

## Internal Design
- Dexie.js wrapper around IndexedDB with encrypted stores for patient sessions, frames, and annotation layers.
- Service Worker intercepts network requests (fetch, XMLHttpRequest) and caches responses; queues POST/PUT/PATCH actions when offline.
- On reconnection, Service Worker processes queued actions in order, with idempotent retries.
- Data stored in IndexedDB is encrypted via WebCrypto before writing; decrypted on read.
- Schema includes tables: sessions, frames, annotations, audit logs, calibration data.
- Versioning handled via Dexie.js version upgrades with migration scripts.

## Interface Contract
See `bento/frontend/subprojects/offline/spec/interface-contract.md`.

## Consumers
- frontend

## Breaking-change Policy
See `bento/frontend/subprojects/offline/spec/interface-contract.md`.

## References
- NFR-8 (Local Network Fault Tolerance)
- NFR-4 (Client Memory Footprint)
- UC-48376 (Load Patient Scan Session)
- UC-47988 (Review Suggested Synovitis Grade)
- UC-25637 (Expose Pixel-Level Activation Logic)
- UC-60739 (Isolate Visual Noise/Artifacts)
- SOFTWARE_SYSTEM_DESIGN_FR_25.md (Section 3.2)
- SOLUTION_ARCHITECTURE_SPEC.md (Section 3.2)
