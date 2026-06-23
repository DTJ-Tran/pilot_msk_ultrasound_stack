# Frontend Specification

## Purpose
Provides interactive clinical workspace, runs edge models (LiteRT, MediaPipe), handles client-side encryption (WebCrypto), offline sync via IndexedDB/Service Worker, and renders UI viewport with graphics adapter fallback.

## Owner
Web Experience Team

## Boundary
PWA service worker, graphics adapter layer (IGraphicsViewport), local browser storage (IndexedDB), and UI components (React, Zustand).

## Internal Design
- Built as a Single Page Application (SPA) using React with TypeScript.
- State managed via Zustand store.
- Client-side encryption via WebCrypto API (AES-256-GCM) before local storage.
- Offline synchronization via Dexie.js (IndexedDB) and Service Worker that queues actions and retries on reconnection.
- Graphics rendering abstracted via IGraphicsViewport interface with WebGLThreeAdapter (Three.js) and CPUSpriteAdapter fallback.
- Edge ML executed in Web Workers: DICOM parser (cornerstone-core), LiteRT angle classifier (MobileNetV4), MediaPipe ROI pre-cropper.
- UI components render multi-layered canvas, workspace controls, diagnostic ribbons, and explanation panels.
- Communication with backend via HTTPS to NGINX gateway, JWT-based authentication, role-based access control (RBAC).

## Interface Contract
See `bento/frontend/spec/interface-contract.md`.

## Consumers
(None)

## Breaking-change Policy
See `bento/frontend/spec/interface-contract.md`.

## References
- NFR-1 (Collaborative Rendering Speed ≤3s)
- NFR-4 (Client Memory Footprint ≤150MB)
- NFR-14 (Legacy Hardware Compatibility)
- UC-48376 (Load Patient Scan Session)
- UC-47988 (Review Suggested Synovitis Grade)
- UC-25637 (Expose Pixel-Level Activation Logic)
- UC-60739 (Isolate Visual Noise/Artifacts)
- SOFTWARE_SYSTEM_DESIGN_FR_25.md (Sections 2.4, 3.1, 3.2, 3.3)
- SOLUTION_ARCHITECTURE_SPEC.md (Section 2.4)
- PROJECT_VIS.md (Section 3.1, 3.2)
