# Offline Interface Contract

## Purpose
Provides offline caching and synchronization for the PWA frontend, enabling continued operation during network interruptions and seamless sync upon reconnection.

## Owner
Web Experience Team (same as frontend)

## Parent
frontend

Boundary
IndexedDB database via Dexie.js, Service Worker for background sync, and local queue for offline actions.

## Provides
- offline cache (IndexedDB storage of encrypted patient sessions, DICOM frames, annotation vectors)
- sync queue (Service Worker-intercepted pending actions)
- local persistence (survives browser reloads, network drops)

## Consumes
(None)

## Consumers
- frontend

## Not Directly Consumable
- frontend internals (e.g., React components, Zustand store)
- backend internals

## Breaking-change Policy
- Changes to IndexedDB schema require version migration scripts.
- Sync protocol changes are backward-compatible; old clients can still sync via tombstone markers.

## References
- NFR-8 (Local Network Fault Tolerance)
- NFR-4 (Client Memory Footprint)
- UC-48376 (Load Patient Scan Session)
- UC-47988 (Review Suggested Synovitis Grade)
- UC-25637 (Expose Pixel-Level Activation Logic)
- UC-60739 (Isolate Visual Noise/Artifacts)
- SOFTWARE_SYSTEM_DESIGN_FR_25.md (Section 3.2)
- SOLUTION_ARCHITECTURE_SPEC.md (Section 3.2)
