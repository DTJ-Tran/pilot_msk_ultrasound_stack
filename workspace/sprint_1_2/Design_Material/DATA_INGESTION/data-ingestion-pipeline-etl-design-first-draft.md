# Data Ingestion Pipeline ETL First Draft Plan — VKIST MSK Sprint 1_2

## Plan Status
- Source plan file requested: `.kilo/plans/data-ingestion-pipeline-etl-first-draft-plan.md`
- Requested source plan file was missing in workspace.
- This file is now the implementation source of truth for the Data Ingestion ETL plan.
- Primary ingestion design source: `PILOT_PROJECT/workspace/sprint_1_2/Design_Material/DATA-INGESTION/data-ingestion-pipeline-etl-first-draft-plan.md`
- OOP/data-concept source of truth: `PILOT_PROJECT/workspace/sprint_1_2/Design_Material/data_engineering/OOP_DATA_ENGINEERING_SPEC.md`

---
## Goal
Design and implement a small-first, incrementally scalable Data Ingestion ETL pipeline for VKIST MSK Sprint 1_2.

The ingestion design must match the OOP data and concept model in `OOP_DATA_ENGINEERING_SPEC.md`, especially:
- Core domain objects
- Runtime agents/services
- Workflow
- SQLite metadata model
- Cloud object storage layout
- API contract objects
- Validation rules
- Sprint 1_2 acceptance criteria

Target path:
```text
DICOM/image upload → secure artifact storage → frame extraction → preprocessing → vision inference → structured result objects → SQLite metadata → S3-compatible artifact refs → browser mask preview
```

---
## Source Context
### Ingestion Design Context
Use `PILOT_PROJECT/workspace/sprint_1_2/Design_Material/DATA-INGESTION/data-ingestion-pipeline-etl-first-draft-plan.md` as the current ingestion design baseline.

Key ingestion design points:
- ETL phases: `Extract`, `Transform`, `Load`
- Sprint 1_2 PoC stack: FastAPI + SQLite + S3-compatible object store
- Production upgrade path: FastAPI → Redis queue → worker pool → Triton → PostgreSQL/PostGIS + S3 + observability
- No PHI in filenames, object keys, URLs, logs, telemetry, or response paths
- UUID-based object keys and artifact references
- Mock and real PyTorch/Triton-compatible inference adapters
- Stable API responses with `session_id`, `job_id`, `trace_id`, and `audit_hash`

### OOP Data Engineering Context
Use `PILOT_PROJECT/workspace/sprint_1_2/Design_Material/data_engineering/OOP_DATA_ENGINEERING_SPEC.md` as the data/concept source of truth.

Sprint 1_2 scope:
```text
DICOM/image upload → frame extraction → preprocessing → vision inference → structured result objects → SQLite metadata → cloud object storage artifact refs → browser mask preview
```

Sprint 1_2 includes:
- Single-frame DICOM upload
- Standard image upload fallback
- SQLite for structured metadata
- Cloud object service for binary artifacts
- FastAPI API contracts
- PyTorch-compatible inference adapters
- Structured OOP domain model for sessions, frames, jobs, predictions, masks, measurements, and audit records

Sprint 1_2 excludes:
- Multi-frame DICOM series
- Triton runtime
- GraphRAG
- EMR sync
- Socratic safety agents
- Full PWA workspace
- Collaboration/annotations

---
## OOP Boundary
```text
Domain objects = clinical and analysis facts.
Agents/services = runtime workers that transform facts.
Repositories = SQLite persistence adapters.
Artifact stores = S3-compatible binary storage adapters.
Orchestrators = coordinate use cases and workflow state.
```

---
## Required Domain Objects
The Data Ingestion design must produce, persist, or reference these OOP objects from `OOP_DATA_ENGINEERING_SPEC.md`.

### Clinical/session objects
- `ClinicianUser`
- `PatientCase`
- `DiagnosticSession`
- `ReviewDecision`
- `AuditLedgerEntry`

### Ingestion/artifact objects
- `ImageAsset`
- `ScanFrame`
- `Calibration`
- `ArtifactReference`

### Analysis/job objects
- `AnalysisJob`
- `PipelineStep`
- `ModelRegistryEntry`
- `ModelArtifact`
- `PreprocessedImage`

### Prediction/result objects
- `AnglePrediction`
- `InflammationPrediction`
- `SegmentationMask`
- `Measurement`
- `SynovitisGrade`

---
## Required Runtime Agents / Services
The ingestion implementation must align with these runtime roles from `OOP_DATA_ENGINEERING_SPEC.md`.

- `DICOMIngestAgent`
  - `accept_upload(file) -> ImageAsset`
  - `extract_frame(image_asset) -> ScanFrame`
  - `extract_calibration(image_asset) -> Calibration`

- `ImageUploadIngestAgent`
  - `accept_upload(file) -> ImageAsset`
  - `build_scan_frame(image_asset) -> ScanFrame`

- `FramePreprocessor`
  - CLAHE, resize, normalization, tensor preparation

- `AngleValidatorAgent`
  - Predicts `AnglePrediction`
  - Validates supported angle branch

- `ROICropperAgent`
  - Optional PoC/no-op first

- `VisionPipelineAgent`
  - Coordinates `run(session_id, frame_id) -> AnalysisJob`

- `InferenceRunner`
  - Loads and runs PyTorch-compatible adapters

- `MeasurementAgent`
  - Converts mask pixels to mm using `Calibration`

- `SeverityScorerAgent`
  - Maps measurements to `SynovitisGrade`

- `ModelRegistryAgent`
  - Selects approved model names and versions

- `ArtifactStoreAgent`
  - Stores raw and derived artifacts
  - Returns `ImageAsset` / `ArtifactReference`

- `LedgerWriterAgent`
  - Appends immutable `AuditLedgerEntry`

---
## ETL Design Aligned to OOP Objects

### Phase 1 — Extract
Purpose:
Accept upload, quarantine, hash, store raw artifact, and create canonical ingestion metadata.

Inputs:
- `POST /api/v1/sessions/{session_id}/frames`
- Single-frame DICOM or standard image upload

Components:
- `UploadController`
- `QuarantineStorage`
- `HashingService`
- `ArtifactStoreAgent`
- `DICOMIngestAgent`
- `ImageUploadIngestAgent`
- `LedgerWriterAgent`

OOP outputs:
- `ImageAsset`
- `ScanFrame`
- `Calibration`
- `AuditLedgerEntry`

Validation:
- Accept single-frame DICOM
- Extract pixel array
- Extract pixel spacing if available
- Accept common image formats
- Generate synthetic/fallback calibration for standard images
- Reject unreadable DICOM
- No PHI in filenames, object keys, URLs, logs, telemetry, or response paths

### Phase 2 — Transform
Purpose:
Convert the extracted frame into clinical analysis facts.

Components:
- `AnalysisJobOrchestrator`
- `FramePreprocessor`
- `AngleValidatorAgent`
- `ROICropperAgent`
- `InferenceRunner`
- `MeasurementAgent`
- `SeverityScorerAgent`
- `SafetyRouter`

OOP outputs:
- `AnalysisJob`
- `PipelineStep`
- `PreprocessedImage`
- `AnglePrediction`
- `InflammationPrediction`
- `SegmentationMask`
- `Measurement`
- `SynovitisGrade`
- `AuditLedgerEntry`

Validation:
- Every result links to `analysis_job_id`
- Mask artifact links to `artifact_id`
- Measurements use calibration when available
- Grade range is `0..3`
- Unsupported angle, low confidence, missing calibration, or artifact correction flags are preserved

### Phase 3 — Load
Purpose:
Persist structured facts and return safe artifact references.

Components:
- `SQLiteMetadataRepository`
- `ArtifactReferenceBuilder`
- `AnalysisResultAssembler`
- `AuditHashBuilder`
- `ObservabilityEmitter`

OOP outputs:
- Stable API response
- Browser mask preview refs
- Immutable audit chain

Validation:
- Every structured object has UUID primary key
- Every analysis result links to `session_id` and `job_id`
- Every audit entry has `audit_hash`
- Audit hash inputs include:
  - `session_id`
  - `job_id`
  - model versions
  - prediction IDs
  - artifact hashes
  - review decision when present

---
## SQLite Metadata Alignment
Use the Sprint 1_2 SQLite model from `OOP_DATA_ENGINEERING_SPEC.md:1058`.

Required tables:
- `diagnostic_sessions`
- `image_assets`
- `scan_frames`
- `calibrations`
- `analysis_jobs`
- `pipeline_steps`
- `model_registry`
- `model_artifacts`
- `angle_predictions`
- `inflammation_predictions`
- `segmentation_masks`
- `measurements`
- `synovitis_grades`
- `review_decisions`
- `audit_ledger_entries`

Additive PoC columns allowed by ingestion design:
- `analysis_jobs.trace_id`
- `analysis_jobs.idempotency_key`
- `pipeline_steps.error_code`
- `audit_ledger_entries.previous_hash`

Do not add PHI-bearing columns or original filenames as required fields.

---
## Object Storage Alignment
Use the UUID-only storage layout from `OOP_DATA_ENGINEERING_SPEC.md:1240`.

```text
s3://vkist-poc/
  sessions/
    {session_id}/
      source/
        {asset_id}.dcm
        {asset_id}.png
      frames/
        {frame_id}.png
      masks/
        {mask_id}.png
      preprocessed/
        {preprocessed_id}.npy
      audit/
        {audit_id}.json
```

Ingestion design may include these additional UUID-keyed artifact prefixes:
```text
preprocessed/
overlays/
outputs/
```

Rules:
- No patient name in object key
- No raw patient ID in object key
- No timestamp-only object key
- Use UUID for all keys
- Store SHA-256 hash for every artifact
- Store metadata in SQLite
- SQLite/Postgres stores refs only, not binary image payloads

---
## API Contract Alignment
Use the OOP API contract objects from `OOP_DATA_ENGINEERING_SPEC.md:1274`.

Required Sprint 1_2 endpoints:
```text
POST /api/v1/sessions
GET  /api/v1/sessions/{session_id}
POST /api/v1/sessions/{session_id}/frames
POST /api/v1/analysis-jobs
GET  /api/v1/analysis-jobs/{job_id}
GET  /api/v1/analysis-jobs/{job_id}/steps
PATCH /api/v1/sessions/{session_id}/review
```

Create Session Request must include:
```json
{
  "patient_hash": "sha256_patient_hash",
  "case_hash": "sha256_case_hash",
  "clinician_user_id": "uuid"
}
```

Upload Frame Request:
```text
POST /api/v1/sessions/{session_id}/frames
Content-Type: multipart/form-data

file: .dcm or image
```

Upload Frame Response must expose:
- `frame_id`
- `source_asset`
- `calibration`

Analysis Job Response must expose stable objects:
- `job_id`
- `status`
- `angle`
- `inflammation`
- `segmentation_mask`
- `measurements`
- `synovitis_grade`
- safe artifact references