# Sprint 1-2 Architecture Specification

**Sprint:** Sprint 1 (June 15 – June 26) + Sprint 2 (June 29 – July 10)  
**Theme:** "The Fast PoC Baseline" + "Multi-Modal & NLP Integration"  
**Parent Document:** [SOLUTION_ARCHITECTURE_SPEC.md](../SOLUTION_ARCHITECTURE_SPEC.md)

---

## 1. Sprint Scope & Goals

### 1.1 Sprint 1: The Fast PoC Baseline
- Establish interactive end-to-end processing pipeline
- Rapid UI prototype with high-fidelity mockups
- Configure initial FastAPI server pipelines to process raw array matrices
- Output early inference mask previews onto browser-based preview window canvas
- Wire ultrasound image ingest pathways into classification pipeline

### 1.2 Sprint 2: Multi-Modal & NLP Integration
- Embed localized NLP translation modules
- Implement client-side privacy scrubbing masks for Decree 13 compliance
- Configure on-device string parsers to sanitize personal identification tokens
- Deploy multi-modal diagnostic chat system
- Build zero-friction NLP conduits for clinical abbreviations

---

## 2. Architectural Constraints for Sprint 1-2

| Constraint | Implementation |
| --- | --- |
| **Air-Gapped Hospital LAN** | No external cloud processing during normal operation. All inference and storage on-premise via K3s. NFR-16a governs emergency cloud fallback only. |
| **Code & Issue Hosting (NFR-16a exception)** | GitLab CE and Jira run self-hosted on a cloud VM (not SaaS). All code, tickets, and pipeline configs transit over public internet to reach the VM. Compensating controls: no PHI in commits or tickets (pre-push hook + team policy); SSH-only git access with certificate pinning; daily GitLab RDB backup to hospital MinIO (not cloud storage); cloud VM IAM with minimum-role access and 2FA; VM access restricted to hospital whitelisted IPs. This exception is reviewed at PoC sign-off. |
| **Network Bandwidth (10 Mbps max)** | Optimize payload sizes, leverage local caching (IndexedDB, Redis). |
| **DICOM Compliance** | Process DICOM images via pydicom stream over local HTTPS. |
| **Client Memory ≤ 150 MB** | PWA uses React + Zustand + LiteRT (no dedicated GPU required). |
| **Latency ≤ 1.5s for inference** | Heavy ML offloaded to Triton Inference Server with ONNX/TensorRT. |
| **Zero PHI Leakage** | Client-side scrubbing before network transfer; no PHI in Git/Jenkins. |

---

## 3. System Context Diagram (C4) - Sprint 1-2 Scope (FR-25 Synovitis Grading)

```plantuml
@startuml "VKIST_MSK_Sprint1_2_Context_FR25"
!include <C4/C4_Context>

title System Context - Sprint 1-2: FR-25 Synovitis Grading & NLP Integration
' Sprint 1-2 scope: FR-25 only with NLP safety layer
' Active Users: UP5 | Governance: UP1, UP4 | Future: UP6, UP7, UP8

' === ACTORS IN SPRINT SCOPE ===
Person(radiologist, "Diagnostic Radiologist (UP5)", "FR-25: load scan, review AI grade (0-3), confirm/override, finalize & sign, view GradCAM, engage circuit breaker, review RAG evidence")

' === GOVERNANCE / NFR ALIGNMENT ===
Person_Ext(senior_expert, "Healthcare Senior Expert (UP1)", "Governance: clinical protocol validation, MOH guideline approval, model threshold sign-off")
Person_Ext(support_staff, "Support Staff (UP4)", "Registration, case queue management")

' === FUTURE SPRINTS ===
Person_Ext(therapist, "Physical Therapist (UP6)", "Future sprint: prescription parser, 3D mapping, kinetic overlay, patient education")
Person_Ext(ortho_surgeon, "Orthopedic Surgeon (UP7)", "Future sprint: treatment planning, aggregated dashboard, 3D anatomy education")
Person_Ext(patient_caregiver, "Patient & Caregiver (UP8)", "Future sprint: self-monitoring portal, inflammation tracker, medication reminders")

Person(admin, "System Administrator", "K3s deployment, model updates, NGINX failover, Prometheus/Grafana monitoring")

' === SYSTEM ===
System(mpps, "VKIST MSK Processing System\n(FR-25 Sprint 1-2)", "Knee ultrasound AI: angle→inflammation→segmentation\nGrading: synovitis 0-3 with GradCAM\nSafety: Circuit Breaker, BERT drift, RAG-Referee\nNLP: Decree 13 scrubbing, GemmaE2B/MedGemma explanations\nReporting: Circular 46 PDF")

' === EXTERNAL SYSTEMS IN SCOPE ===
System_Ext(pacs, "Hospital PACS / Ultrasound", "DICOM source (C-MOVE + direct capture)")
System_Ext(emr, "Hospital EMR/HIS", "Finalized reports, audit logs (HL7/FHIR)")
System_Ext(triton, "Triton Inference Server", "GPU inference: angle, inflammation, segmentation + embeddings")
System_Ext(knowledge, "Clinical Knowledge Stack", "ladybugDB (ontology), pgvector (MOH guideline vectors in Postgres HNSW), EmbeddingGemma (RAG embedding model), GemmaE2B (browser WebLLM), MedGemma (cloud Vertex AI)")

' === RELATIONSHIPS ===
Rel(radiologist, mpps, "Load scan, review grade, confirm/override, finalize, view explanations, engage safety dialog", "HTTPS")
Rel(admin, mpps, "Deploys, monitors, configures", "HTTPS/SSH")
Rel(senior_expert, mpps, "Validates protocols, approves thresholds", "HTTPS")
Rel(support_staff, mpps, "Registration, case queue", "HTTPS")

Rel(therapist, mpps, "Not in Sprint 1-2 scope", "—")
Rel(ortho_surgeon, mpps, "Not in Sprint 1-2 scope", "—")
Rel(patient_caregiver, mpps, "Not in Sprint 1-2 scope", "—")

Rel(mpps, pacs, "DICOM import", "C-MOVE + upload")
Rel(mpps, emr, "Finalized reports, audit", "HL7/FHIR")
Rel(mpps, triton, "ML inference", "gRPC :8001")
Rel(mpps, knowledge, "RAG + ontology + LLM", "gRPC/HTTP + C++")

@enduml
```

---

## 4. Container Diagram (C4) - Sprint 1-2 Implementation

```plantuml
@startuml "VKIST_MSK_Containers_Sprint1_2"
!include <C4/C4_Container>

title Container Diagram - VKIST MSK Platform (Sprint 1-2)

Person(radiologist, "Radiologist (UP5)", "Performs primary diagnosis, view validation, and severity grading.")
Person(therapist, "Physical Therapist (UP6)", "Observes scans, evaluates kinetic data, and structures physical rehabilitation plans.")

System_Boundary(hospital_lan, "Air-Gapped Hospital LAN (Max 10 Mbps)") {
    
    Container(pwa, "React PWA Frontend", "React, TS, Zustand, LiteRT, MediaPipe, Dexie.js", "Interactive visualization, local WebAssembly inference for view-angle validation, encrypted IndexedDB cache, DICOM upload, edge guardrail (Transformers.js BERT + OpenRedaction + pii-filter) in dedicated WebWorkers")
    
    Container(nginx, "NGINX Reverse Proxy + Keepalived", "NGINX 1.27, Keepalived", "SSL/TLS termination, single VIP, instant failover (<=2s), routes to active FastAPI node")
    
    System_Boundary(backend_servers, "Application Server Cluster") {
        Container(fastapi, "FastAPI Application Server", "Python, Uvicorn, SQLAlchemy, ReportLab", "API orchestration, angle classification routing, inflammation detection, segmentation post-processing, measurement, severity analysis, PDF report generation, client-side scrubbing validation")
        
        System_Boundary(ml_inference, "ML Inference Stack (Sprint 1-2)") {
            Container(triton, "Triton Inference Server", "NVIDIA Triton, ONNX, OpenVINO, TensorRT", "Executes 3-step ML pipeline: angle classification, inflammation detection, segmentation (UNet3+/DeepLabV3)")
            ContainerDb(model_store, "Local Model Store", "ONNX/Torch weights on disk", "Stores model checkpoints mounted read-only into Triton")
        }
        
        System_Boundary(observability, "Observability (Sprint 1-2)") {
            Container(prometheus, "Prometheus", "Prometheus", "Scrapes FastAPI and Triton metrics")
            Container(grafana, "Grafana", "Grafana", "Operational dashboards for inference latency, GPU utilization, cache hit rate")
        }
        
        System_Boundary(data_stack, "Data Stack (Sprint 1-2)") {
            ContainerDb(postgres, "PostgreSQL + PostGIS", "PostgreSQL", "Stores session metadata, EMR records, spatial markers, audit ledger")
            ContainerDb(redis, "Redis Cache", "Redis", "Session state, JWT tokens, rate limiting")
            ContainerDb(s3, "S3 Object Store (MinIO)", "MinIO", "DICOM-derived images, segmentation overlays, Grad-CAM heatmaps, report blobs")
        }
    }
}

Rel(radiologist, pwa, "Uploads DICOM, views overlays, accepts/rejects grades")
Rel(therapist, pwa, "Reviews scan results, annotates feedback")

Rel(pwa, nginx, "HTTPS requests with encrypted DICOM payloads", "HTTPS (Port 443)")
Rel(nginx, fastapi, "Routes API requests", "HTTP/1.1 (Port 8000)")

Rel(fastapi, redis, "Session verification, rate limiting", "TCP (Port 6379)")
Rel(fastapi, postgres, "Metadata, audit ledger, spatial queries", "SQL/TCP (Port 5432)")
Rel(fastapi, s3, "Image and report blob storage", "S3 API")

Rel(fastapi, triton, "Offloads ML inference: angle, inflammation, segmentation", "gRPC (Port 8001)")
Rel(triton, model_store, "Reads model weights", "Local FS")

Rel(prometheus, fastapi, "Request latency, error rate, DB pool", "HTTP /metrics")
Rel(prometheus, triton, "Model latency, VRAM, GPU utilization", "HTTP /metrics")
Rel(grafana, prometheus, "Dashboard queries", "HTTP (Port 9090)")

@enduml
```

---

## 5. Component Diagram (C4) - FastAPI Server Internals (Sprint 1-2)

```plantuml
@startuml "VKIST_MSK_Backend_Components_Sprint1_2"
!include <C4/C4_Component>

title Component Diagram - FastAPI Application Server (Sprint 1-2)

Container_Boundary(backend, "FastAPI Application Server") {
    
    System_Boundary(api_routers, "API Routers") {
        Component(analyze_router, "Analysis Router", "FastAPI Router", "/api/analyze - Main ML pipeline endpoint\nHandles angle model selection, inflammation detection, segmentation routing, measurement, severity analysis")
        Component(save_router, "Save Router", "FastAPI Router", "/api/save - Patient data persistence\nSanitizes metadata, stores images and PDF reports")
        Component(export_router, "PDF Export Router", "FastAPI Router", "/api/export-pdf - On-demand PDF generation")
        Component(health_router, "Health Router", "FastAPI Router", "/api/health - Liveness probe")
    }
    
    System_Boundary(ml_pipeline, "ML Pipeline Components (Sprint 1-2)") {
        Component(angle_classifier, "Angle Classifier", "PyTorch/ONNX", "Classifies ultrasound plane (med-lat, post-trans, sup-trans-flex, sup-up-long)\nModels: ConvNeXt-Tiny, DenseNet-121, ResNet-50, EfficientNet-B2, Swin-V2-S")
        Component(inflammation_detector, "Inflammation Detector", "PyTorch/ONNX", "Binary classifier for inflammation presence\nModel: EfficientNet-B0 (2-class)")
        Component(segmentation_engine, "Segmentation Engine", "PyTorch/ONNX", "Pixel-wise anatomical segmentation\nModels: DeepLabV3-ResNet50/101, UNet-ResNet101, EfficientFeedback, UNet3Plus-Attention")
        Component(measurement_engine, "Measurement Engine", "Python/NumPy/OpenCV", "Calculates synovium thickness in mm, effusion metrics\nPIXEL_TO_MM = 45.0 / 655.0")
        Component(severity_analyzer, "Severity Analyzer", "Python", "Classifies synovitis grade (0-3) with combined effusion+synovium scoring\nGenerates Vietnamese clinical descriptions")
        Component(preprocessor, "Image Preprocessor", "Python/PIL/OpenCV", "CLAHE contrast enhancement, resize, normalize")
        Component(overlay_renderer, "Overlay Renderer", "Python/PIL", "Creates color-coded segmentation overlays with measurement annotations")
    }
    
    System_Boundary(knowledge_stack, "Knowledge Stack (Sprint 2)") {
        Component(nlp_scrubber, "Patient Data Scrubber", "Microsoft Presidio", "Re-verify edge redaction; refine residual PII; error if unresolvable")
            Component(rag_coordinator, "RAG Coordinator", "Python", "Retrieves MOH guideline passages from pgvector (PostgreSQL HNSW index); mandatory pre-generation retrieval for all LLM tiers (browser WebLLM and cloud MedGemma)")
        Component(ontology_query, "Ontology Query Engine", "C++ bindings", "ladybugDB graph traversal for anatomical entity relationships")
        Component(guardrail_edge, "Edge Guardrail", "Transformers.js BERT", "Client-side hallucination/mal-intention/scope-breach scoring; triggers session termination + cloud mitigate via FastAPI guardrail-check endpoint")
        Component(referee, "RAG-Referee", "BERT classifier", "Server-side 3-axis citation contestant validation (attribution, cohesion, factual contestant status)")
    }
    
    System_Boundary(reporting, "Reporting & Audit") {
        Component(pdf_generator, "PDF Report Generator", "ReportLab", "Bilingual (VI/EN) medical reports per Circular 46/2018/TT-BYT")
        Component(audit_logger, "Immutable Audit Logger", "SQLAlchemy/Postgres", "Append-only clinical decision and AI interaction logs\nPrevents UPDATE/DELETE via DB triggers")
    }
    
    System_Boundary(infrastructure, "Infrastructure") {
        Component(cache_client, "Redis Client", "redis-py", "Session state, JWT tokens, rate limiting")
        Component(storage_client, "S3 Client", "boto3", "DICOM images, overlays, reports, Grad-CAM heatmaps")
        Component(db_client, "PostgreSQL Client", "SQLAlchemy", "Relational/spatial queries, audit ledger")
        Component(triton_client, "Triton gRPC Client", "gRPC", "Inference offloading for heavy ML models")
    }
}

' Internal relationships
Component(analyze_router, preprocessor, "Uploads image, applies CLAHE")
Component(analyze_router, angle_classifier, "Classifies angle plane")
Component(analyze_router, inflammation_detector, "Detects inflammation (if post-trans or sup-up-long)")
Component(analyze_router, segmentation_engine, "Runs segmentation (if inflammation detected)")
Component(analyze_router, measurement_engine, "Measures thickness (sup-up-long only)")
Component(analyze_router, severity_analyzer, "Grades synovitis severity")
Component(analyze_router, overlay_renderer, "Generates visualization overlay")

Component(save_router, nlp_scrubber, "Validates scrubbing before save")
Component(save_router, pdf_generator, "Triggers PDF generation")
Component(save_router, audit_logger, "Logs save action immutably")

Component(export_router, pdf_generator, "Generates on-demand PDF")

Component(rag_coordinator, triton_client, "RAG embedding extraction via Triton (EmbeddingGemma)")
Component(rag_coordinator, ontology_query, "Graph traversal for evidence")
Component(rag_coordinator, referee, "Mandatory RAG-Referee validation per axis")
Component(guardrail_edge, "Edge Guardrail", "Transformers.js BERT", "Scores hallucination/mal-intention/scope-breach in WebWorker")
Component(guardrail_edge, referee, "Violation signal → server-side referee gate")

' Infrastructure connections
Component(analyze_router, cache_client, "Session validation")
Component(analyze_router, storage_client, "Image/report I/O")
Component(analyze_router, db_client, "Metadata, audit")
Component(analyze_router, triton_client, "ML inference offload")

@enduml
```

---

## 6. Deployment Diagram (C4) - Sprint 1-2 Hospital LAN Runtime

```plantuml
@startuml "VKIST_MSK_Deployment_Sprint1_2"
!include <C4/C4_Deployment>

title Deployment Diagram - VKIST MSK Platform (Sprint 1-2)

Deployment_Node(hw, "Hospital On-Premise Hardware\n(Dell PowerEdge / Local Server)") {
    Deployment_Node(k8s_alt, "K3s Runtime (Sprint 1-2)") {
        Deployment_Node(nginx_node, "NGINX Container") {
            Container(nginx_c, "NGINX 1.27 + Keepalived", "Reverse proxy, SSL, VIP failover")
        }
        Deployment_Node(fastapi_node, "FastAPI Container") {
            Container(fastapi_c, "FastAPI Uvicorn", "Python app: analysis, save, export, NLP scrub, RAG")
        }
        Deployment_Node(prom_node, "Prometheus Container") {
            Container(prom_c, "Prometheus", "Metrics collection")
        }
        Deployment_Node(grafana_node, "Grafana Container") {
            Container(graf_c, "Grafana", "Dashboards")
        }
    }
    
    Deployment_Node(vm_db, "Database / Storage VM") {
        Deployment_Node(pg_node, "PostgreSQL + pgvector Node") {
            ContainerDb(pg_c, "PostgreSQL + PostGIS + pgvector", "Primary DB, vector HNSW index, audit ledger")
        }
        Deployment_Node(redis_node, "Redis Node") {
            ContainerDb(redis_c, "Redis", "Session cache, rate limit")
        }
        Deployment_Node(s3_node, "MinIO Node") {
            ContainerDb(s3_c, "MinIO S3", "Object storage for images and reports")
        }
    }
    
    Deployment_Node(triton_hw, "Inference Server (GPU Node)") {
        Deployment_Node(triton_node, "Triton Container") {
            Container(triton_c, "Triton Inference Server", "ONNX/TensorRT models, ensemble pipelines")
        }
        Deployment_Node(model_vol, "Model Volume") {
            ContainerDb(model_c, "Model Weights", "Read-only mount: .pth / .onnx files")
        }
    }
}

Deployment_Node(client, "Clinician Workstation / Tablet") {
    ContainerDb(browser, "Browser PWA", "React, Service Worker, IndexedDB")
}

Rel(browser, nginx_c, "HTTPS (port 443)", "TLS 1.3")
Rel(nginx_c, fastapi_c, "HTTP (port 8000)", "Internal LAN")
Rel(fastapi_c, pg_c, "SQL/TCP (port 5432)", "LAN")
Rel(fastapi_c, s3_c, "S3 API", "LAN")
Rel(fastapi_c, triton_c, "gRPC (port 8001)", "LAN (or same host)")

Rel(prom_c, fastapi_c, "/metrics scrape", "HTTP")
Rel(prom_c, triton_c, "/metrics scrape", "HTTP")
Rel(graf_c, prom_c, "Dashboard", "HTTP")

Rel(triton_c, model_vol, "Loads weights", "Read-only FS")

Rel(browser, browser, "Local-only WebAssembly inference (LiteRT/MediaPipe)", "No network")

@enduml
```

---

## 7. Sprint 1-2 ML Workflow: Ultrasound Processing Pipeline

```plantuml
@startuml "VKIST_MSK_ML_Pipeline_Sprint1_2"
@startuml
title ML Pipeline - Knee Ultrasound Analysis (Sprint 1-2)

start

:Clinician uploads DICOM via PWA;
:PWA encrypts payload, sends over HTTPS;

:NGINX routes to active FastAPI node;

:FastAPI receives image;
:Apply CLAHE preprocessing (contrast enhancement);

:RUN ANGLE CLASSIFICATION;
:Model: ConvNeXt/DenseNet/ResNet/EfficientNet/Swin-V2;
:Classes: med-lat, post-trans, sup-trans-flex, sup-up-long;

if (Angle class?) then (post-trans)
    : Inflammation Detection;
    :Model: EfficientNet-B0 (binary);
    if (Inflammation?) then (yes)
        :Post-Trans Segmentation;
        :Model: DeepLabV3-ResNet101;
        :Classes: fat, tendon, muscle, femur, artery, synovium, baker's cyst;
        :Generate segmentation masks;
        :Create overlay image;
    else (no)
        :Skip segmentation;
        :Set severity = 0;
    endif
elseif (sup-up-long)
    : Inflammation Detection;
    if (Inflammation?) then (yes)
        :Suprapatellar Segmentation;
        :Model: UNet3Plus-Attention / DeepLabV3 / EfficientFeedback;
        :Classes: effusion, fat, fat-pat, femur, synovium, tendon;
        :Generate segmentation masks;
        
        :Measure Synovium Thickness;
        :ROI: middle 1/3 of bounding box;
        :Unit: mm (PIXEL_TO_MM = 45/655);
        
        :Create overlay with measurement annotations;
        
        :Analyze Severity;
        :Combined score: effusion (60%) + synovium (40%);
        :Grade: 0 (Rất nhẹ) / 1 (Nhẹ) / 2 (Trung bình) / 3 (Nặng);
    else (no)
        :Skip segmentation and measurement;
        :Set severity = 0;
    endif
else (other angles)
    :Only angle classification result returned;
endif

:Generate enhanced image (CLAHE);
:Assemble JSON response with overlays, masks, measurements, severity;

if (Save requested?) then (yes)
    :NLP Scrubber validates Decree 13 compliance;
    :Store images to MinIO S3;
    :Store metadata to PostgreSQL;
    :Append immutable audit log;
    :Generate bilingual PDF report;
endif

:Return response to PWA;

stop

@enduml
```

---

## 8. Data Flow Diagram (Activity View)

```plantuml
@startuml "VKIST_MSK_DataFlow_Sprint1_2"
title Data Flow - VKIST MSK Platform (Sprint 1-2)

|PWA Client|
start
:Upload DICOM image;
:Apply CLAHE preprocessing locally;
:Encrypt payload;
:Send HTTPS POST to /api/analyze;

|NGINX Gateway|
:Receive request;
:SSL termination;
:Route to active FastAPI node;

|FastAPI Server|
:Receive image;
:Validate JWT + RBAC;
:Load angle classifier model;
:Run angle classification;
if (Angle class?) then (post-trans)
  :Load inflammation detector;
  :Run inflammation detection;
  if (Detected?) then (yes)
    :Load post-trans segmentation model;
    :Run DeepLabV3-ResNet101 inference via Triton;
    :Receive masks from Triton;
    :Create segmentation overlay;
    :Return JSON with overlay + masks;
  else (no)
    :Return JSON with angle + inflammation only;
  endif
elseif (sup-up-long)
  :Load inflammation detector;
  :Run inflammation detection;
  if (Detected?) then (yes)
    :Load suprapatellar segmentation model;
    :Run UNet3Plus-Attention inference via Triton;
    :Receive masks from Triton;
    :Measure synovium thickness (ROI middle 1/3);
    :Calculate effusion metrics;
    :Analyze severity (0-3 combined score);
    :Create overlay with measurement annotations;
    :Return JSON with overlay + measurement + severity;
  else (no)
    :Return JSON with angle + inflammation only;
  endif
else (other)
  :Return angle classification only;
endif

|PWA Client|
:Receive JSON response;
:Display enhanced image + overlays;
:Render measurement annotations;
:Show severity grade with color coding;

if (User action: Save?) then (yes)
  |PWA Client|
  :Run NLP scrubber (Decree 13);
  :Remove PII from metadata;
  :Send HTTPS POST to /api/save;
  
  |FastAPI Server|
  :Validate scrubbing compliance;
  :Store images to MinIO S3;
  :Store metadata to PostgreSQL;
  :Append immutable audit log;
  :Generate bilingual PDF report (Circular 46);
  :Return success + folder path;
  
  |PWA Client|
  :Confirm save to user;
endif

stop

@enduml
```

---

## 9. Non-Functional Requirements Coverage (Sprint 1-2)

| NFR | Sprint 1-2 Implementation |
| --- | --- |
| **NFR-1** (DICOM Speed ≤ 3.0s) | Local Triton inference + Redis caching of recent sessions |
| **NFR-4** (Client Memory ≤ 150 MB) | React PWA with Zustand; LiteRT WebAssembly (no GPU); Dexie.js for local cache |
| **NFR-5** (Inference ≤ 1.5s) | Triton with TensorRT/OpenVINO quantization; ONNX runtime |
| **NFR-6** (VRAM ≤ 2 GB) | Quantized ONNX models; batch size 1; DeepLabV3-ResNet101 optimized |
| **NFR-7** (UI Refresh ≤ 200ms) | Token streaming via SSE; frontend state updates async |
| **NFR-8** (Fault Tolerance) | IndexedDB local cache; service worker offline mode; session recovery |
| **NFR-9** (Availability ≥ 99.9%) | NGINX + Keepalived active-passive VIP; Docker restart policies |
| **NFR-10** (Generative Safety) | Edge guardrail: prompt rules + BERT detection (hallucination/mal-intention/scope-breach) → session termination → cloud mitigate (Vertex AI). Mandatory RAG pre-processing for all LLM tiers (not optional tool calling). RAG-Referee citation contestant validation (3-axis). Server-side Decree 13 redaction ground-check before Vertex AI egress. |
| **NFR-11** (Onboarding ≤ 45 min) | High-fidelity Figma prototypes in Sprint 1; structured workflows |
| **NFR-13** (Grad-CAM Zero-Click) | Overlay rendered directly on upload; zero extra UI steps |
| **NFR-14** (No client GPU) | PWA falls back to CPU-bound rendering; LiteRT for lightweight inference |
| **NFR-16** (Air-Gapped) | Entire inference and storage stack on-premise via K3s; no external cloud for clinical data. NFR-16a exception: GitLab/Jira on cloud VM with compensating controls. |
| **NFR-17** (Immutable Audit) | PostgreSQL triggers prevent UPDATE/DELETE on audit tables |
| **NFR-18** (RAG Citations) | pgvector retrieves MOH guideline passages (PostgreSQL HNSW index); LLM generates footnoted explanations |
| **NFR-19** (HITL Gate) | Database state machine prevents FINALIZED status without clinician digital signature |

---

## 10. Key Decree 13 / Circular 46 Compliance (Sprint 2)

### 10.1 Decree 13/2023/ND-CP - Personal Data Protection
- Client-side scrubbing via `nlp_scrubber` component before any network transfer
- Regex-based PII removal (names, IDs, phone numbers) in browser
- No PHI stored in Git, Jenkins artifacts, or external systems

### 10.2 Circular 46/2018/TT-BYT - EMR Compliance
- PDF reports generated per official MOH format (bilingual VI/EN)
- Audit trail immutable via database triggers
- Reports stored with cryptographic checksums in MinIO

---

## 11. Infrastructure Decisions (Sprint 1-2)

| Decision | Choice | Rationale |
| --- | --- | --- |
| **Orchestration** | K3s (Kubernetes-certified, lightweight edge distribution) | Chosen over Docker Compose, Docker Swarm, Nomad, ECS Fargate, Cloud Run. NFR-16 requires on-premise, eliminating cloud-only options. Docker Swarm offers lowest PoC cost but is in maintenance mode with highest migration overhead. K3s is already production-grade; scaling path is multi-cluster federation, not platform replacement. |
| **CI/CD** | Jenkins on hospital K3s | Runs inside trusted LAN; connects to cloud-hosted GitLab for source. No external build triggers. |
| **Code Hosting** | Self-hosted GitLab CE on cloud VM (NFR-16a exception) | Reliability over hospital-hardware self-hosting; not SaaS. Compensating controls: no PHI in commits (pre-push hook), SSH-only access with cert pinning, daily RDB backup to hospital MinIO, cloud IAM with 2FA + minimum-role, IP whitelist to hospital networks. Exception reviewed at PoC sign-off. |
| **Issue Tracking** | Self-hosted Jira on same cloud VM (NFR-16a exception) | Clinical feedback and tickets stay within controlled access boundary. No PHI in tickets per team policy. Same compensating controls as GitLab. |
| **Model Serving** | Triton Inference Server | ONNX/TensorRT support; ensemble pipelines; HTTP/gRPC |
| **Reverse Proxy** | NGINX + Keepalived | VIP for high availability; SSL termination; instant failover |
| **Local LLM** | Browser WebLLM (GemmaE2B) + Cloud MedGemma (Vertex AI) | Browser: Vietnamese + clinical language support, local inference (air-gapped). Cloud: MedGemma for NFR-16a fallback + BERT-triggered arbiter. Triton hosts CV models + EmbeddingGemma only. |
| **Vector Search** | pgvector (PostgreSQL HNSW index) | Already deployed with Postgres; zero additional infrastructure; ~15K MOH vectors at ~5-20ms query latency fits NFR-7. Complex SQL filtering for clinical queries. Qdrant deferred to Phase 2. |
| **Ontology DB** | ladybugDB embedded | C++ library embedded in FastAPI process; SNOMED-CT/LOINC mappings |

---

## 12. Technology Stack Summary

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend | React, TypeScript, Zustand, Dexie.js, LiteRT, MediaPipe, Transformers.js, OpenRedaction, pii-filter, js-data-anonymizer | PWA with offline support, local inference, and edge guardrail (BERT hallucination/mal-intention detection, Decree 13 PII scrubbing) |
| Guardrail | Transformers.js BERT (WebWorker), OpenRedaction, pii-filter, js-data-anonymizer, FastAPI `phi_scrub` middleware, Vertex AI Model Garden safety filters | Edge behavior control without NeMo/GuardrailsAI; prompt-rule + BERT detection; session termination + cloud mitigate; mandatory RAG pre-processing (not optional tool-call); server-side redaction ground-check before NFR-16a egress |
| Gateway | NGINX 1.27 + Keepalived | SSL termination, VIP, load balancing |
| API | FastAPI, Uvicorn, SQLAlchemy, ReportLab | REST API, ORM, PDF generation |
| ML Inference | Triton, ONNX, TensorRT, OpenVINO | Model serving with quantization |
| Models | ConvNeXt, DenseNet, ResNet, EfficientNet, Swin-V2, UNet3Plus, DeepLabV3 | Angle, inflammation, segmentation |
| Data | PostgreSQL + PostGIS, MinIO, Redis | Relational, object, cache |
| Knowledge | pgvector, ladybugDB, GemmaE2B/MedGemma, EmbeddingGemma, BioClinicalBERT | RAG (pgvector HNSW), ontology (ladybugDB), Vietnamese/clinical LLM, 768-dim RAG embeddings, BERT drift/referee |
| Observability | Prometheus, Grafana | Metrics and dashboards |
| Code Hosting | Self-hosted GitLab CE (cloud VM, NFR-16a exception) | Source control, issue tracking, merge requests, container registry |
| CI/CD | Jenkins on hospital K3s | Build, test, deploy pipeline; connects to cloud-hosted GitLab |

---

## 13. Cross-References

| Document | Relevance |
| --- | --- |
| [SOLUTION_ARCHITECTURE_SPEC.md](../SOLUTION_ARCHITECTURE_SPEC.md) | Main architecture spec, NFR definitions, pattern citations, trade-off analysis |
| [Backend Specification](CODEBASE/backend/spec/backend-spec.md) | FastAPI server internal design, API contracts, RAG coordinator |
| [Knowledge Stack Specification](CODEBASE/knowledge/spec/knowledge_spec.md) | Qdrant/ladybugDB schema, embedding models, LLM endpoints |
| [CI/CD Deployment Pipeline](Design_Material/CI_CD_docs/CI_CD_DEPLOYMENT_PIPELINE.md) | Jenkins pipeline, Docker Compose runtime, offline bundles, rollback |
| [DATA_SPEC.md](CODEBASE/data/spec/data_spec.md) | Data contracts, schema definitions |
| [CONTEXT_VISION_SCOPE.md](../../PROJ_LEVEL_READING/PLAN/CONTEXT_VISION_SCOPE.md) | Project vision, sprint timelines, user personas |

---

## 14. Design Decisions

| # | Decision | Alternatives Considered | Rationale |
| --- | --- | --- | --- |
| 1 | Triton for model serving | TorchServe, FastAPI direct | Triton supports ONNX/TensorRT ensembles, dynamic batching, and concurrent model execution |
| 2 | K3s over Docker Compose/Swarm/Nomad/ECS/Cloud Run | Docker Compose, Docker Swarm, Nomad, ECS Fargate, Cloud Run | NFR-16 requires on-premise, eliminating cloud-only platforms (ECS, Cloud Run). Docker Swarm is in maintenance mode with highest migration cost to production. K3s is already production-grade; scaling to N hospitals is multi-cluster federation, not platform replacement. |
| 3 | MinIO over AWS S3 | Direct filesystem, NFS | S3-compatible API allows future cloud migration; object versioning built-in |
| 4 | pgvector over Qdrant/Pinecone | Qdrant, Pinecone, Weaviate | Postgres already deployed; pgvector adds zero infrastructure overhead. At ~15K MOH guideline vectors, HNSW query latency (~5-20ms in shared_buffers) fits within NFR-7 budget. Qdrant advantage appears at millions of vectors or >500 QPS; not needed at PoC scale. Phase 2: introduce Qdrant if corpus exceeds ~100K vectors. |
| 5 | ladybugDB embedded | Separate graph DB service | Embedded C++ library reduces latency; no separate process to manage |

---

## 15. Open Questions / Future Work (Post Sprint 2)

| ID | Question | Target Sprint |
| --- | --- | --- |
| Q1 | How to handle concurrent clinician sessions with shared Triton GPU? | Sprint 3 |
| Q2 | Should model weights be versioned in PostgreSQL for A/B testing? | Sprint 4 |
| Q3 | How to integrate DICOM C-STORE for automatic PACS ingestion (currently C-MOVE only)? | Sprint 5 |
| Q4 | Will GemmaE2B be swapped for MedGemma or Willa when hospital provides GPU cluster? | Sprint 5 |
| Q5 | Should Prometheus scrape endpoints be authenticated for NFR-17 audit compliance? | Sprint 3 |
