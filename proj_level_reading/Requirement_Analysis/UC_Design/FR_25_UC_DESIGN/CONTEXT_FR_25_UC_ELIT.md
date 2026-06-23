BELOW is the consolidated structural baseline engineering reference document tracking all architectural constraints, system interactions, and discovered sub-components for the **FR-25 Synovitis Grading Engine**.

---

# Context_FR_25_UC.md

## 1. Context, Mission Boundary & Core Rationale

### 1.1 Scope Identification

* **Target Core Functional Requirement:** `FR-25` (ULTS-Đánh giá và phân cấp mức độ viêm màng hoạt dịch / Synovitis Grading Engine).
* **Primary System Boundary:** The workspace acts as a strict secure diagnostic execution wrapper. In order to manage systemic liability and avoid black-box compliance failures, the advanced multi-agent checking modules (**LLM Explainer**, **BERT Hallucination Detector**, and **RAG-Referee**) are restricted from handling generic application operations. They are encapsulated entirely as **Internal Layered Workspace Subsystems** dedicated exclusively to validating human-AI coordination logs for `FR-25`.

### 1.2 Engineering Value Optimization

* **The Clinical Chasm:** In high-volume Vietnamese public clinics, specialists face intensive shift demands often exceeding 100 scans daily. Basic AI setups risk inducing automated checklist fatigue or introducing catastrophic blindness loops if human clinicians simply blind-concur with machine estimations.
* **The System Solution:** By engineering clear internal state boundaries separating standard CRUD processing from multi-tier validation agents, the system systematically handles four concurrent behavioral quadrants. It forces explicit human verification loops during disagreements, cross-references findings against un-biased clinical knowledge nodes, and maintains diagnostic speed metrics without degrading data correctness limits.

---

## 2. Structural Actor Profile Mapping

| Actor Name | Canonical Identifier | Role Scope & Operational Profile within FR-25 Boundary |
| --- | --- | --- |
| **Diagnostic Radiologist** | `Rad (UP5)` | **Primary Human Actor:** National-level clinical expert (Specialist II / Professor, age 40–60+). Holds ultimate medical accountability; validates and signs off pixel segmentations, metrics, and grading summaries. |
| **Hospital EMR System** | `EMR` | **External System Actor:** Recipient database server. Receives finalized JSON structures and signed clinical data logs over localized network pipes post human validation. |
| **VKIST Vision Grader Engine** | `Grader` | **External System Actor:** Foundation deep-learning array (ConvNeXt/MedSAM). Ingests raw frame parameters and produces pixel segmentations, thickness markers (mm), and classification tensors. |

---

## 3. Discovered Use Cases (4-Quadrant Framework)

### 3.1 Core Image Data Intake & Workflow Baselines

* **`UC-48376` (Load Patient Scan Session):** Ingests incoming image frames, maps spatial structures, and activates local session states.
* **`UC-47988` (Review Suggested Synovitis Grade):** Renders the initial classification summary panel (Grades 0-3) alongside color-coded segmentation overlaps.
* **`UC-92006` (Finalize & Sign Electronic Record):** Seals the session data via localized human cryptographic signing steps before dispatching payload JSON logs to the hospital storage sinks.

### 3.2 Quadrant 1: True Agreement Flow (AI Correct / Doctor Correct)

* **`UC-25776` (Generate GradCAM & CoT Explanation Panel):** The internal LLM Explainer checks raw pixel masks and maps multi-modal prompt matrices to output clear, human-scannable rationales.
* **`UC-02423` (Log High-Trust Concur Block):** Encapsulates the corresponding Chain-of-Thought logs confirming human-machine consensus into a structured block to verify system state traceability.

### 3.3 Quadrant 2: Automation Override Risk Loop (AI Correct / Doctor Oversight)

* **`UC-22159` (Trigger Conversational Circuit Breaker):** Intercepts standard workspace finalization pathways if high mouse click adjustments or text conflict markers indicate user friction or ambiguity.
* **`UC-55146` (Facilitate Socratic Reasoning Dialogue):** Initiates an inline workspace chat panel, prompting the specialist to evaluate spatial discrepancies or vascular metrics versus the machine's model inputs.
* **`UC-74821` (Monitor Drift via BERT Sub-Layer):** Scans active conversation tokens continuously to detect illogical claims or contextual drift during active discussion.
* **`UC-65473` (Arbitrate Evidence via RAG-Referee):** Intervenes if human-machine disputes reach an impasse, bypassing active chat logs to pull verified medical guidelines directly from fixed reference sources.

### 3.4 Quadrant 3: Clinician Subservience Risk Loop (AI Hallucinates / Doctor Correct)

* **`UC-25637` (Expose Pixel-Level Activation Logic):** Displays granular layer activations and weight scores when a clinician actively contests a machine grade suggestion.
* **`UC-60739` (Isolate Visual Noise/Artifacts):** Provides on-screen cursor brushes for the specialist to isolate and mask out clutter variables like acoustic shadowing or bone scattering.
* **`UC-62864` (Commit Validated Ground-Truth Record):** Re-runs data logs through the verification referee, updating final reports to show human superiority while saving the masked framework for subsequent model training runs.

### 3.5 Quadrant 4: Double Blind Failure Loop (AI Faulty / Doctor Biased)

* **`UC-35956` (Activate Clinical Investigation Mode):** Transitions the user interface environment instantly to a strict manual tracking orientation when low vision confidence values align with zero-match RAG search responses.
* **`UC-47796` (Execute Structured Morphology Annotation):** Displays a standardized template forcing manual plotting of novel structural modifications or unrecognized lesion variations.
* **`UC-01580` (Serialize Session to Telemetry Queue):** Packages unencrypted image tensors, coordinate indices, and clinical commentary blocks into localized storage pipelines, bypassing standard EMR charts to flag data directly for software engineering team review.

---

## 4. Master PlantUML System Compilation

```plantuml
@startuml
' Settings & Aesthetic Optimization
left to right direction
skin rose

' External Actors
actor "Diagnostic Radiologist (UP5)" as Rad
actor "Hospital EMR System" as EMR << System >>
actor "VKIST Vision Grader Engine" as Grader << System >>

' System Boundary
rectangle "VKIST MSK Workspace (FR-25: Synovitis Grading Scope)" {
    
    ' Core Viewing & Data Intake Pipelines
    usecase "Load Patient Scan Session" as UC-48376
    usecase "Review Suggested Synovitis Grade (0-3)" as UC-47988
    usecase "Finalize & Sign Electronic Record" as UC-92006
    
    ' Sub-Boundary for the Internal Cognitive/Multi-Agent Subsystems
    rectangle "Internal Cognitive & Validation Stack" {
        
        ' Q1: True Agreement Use Cases
        usecase "Generate GradCAM & CoT Explanation Panel" as UC-25776
        usecase "Log High-Trust Concur Block" as UC-02423
        
        ' Q2: Automation Override Risk Use Cases
        usecase "Trigger Conversational Circuit Breaker" as UC-22159
        usecase "Facilitate Socratic Reasoning Dialogue" as UC-55146
        usecase "Monitor Drift via BERT Sub-Layer" as UC-74821
        usecase "Arbitrate Evidence via RAG-Referee" as UC-65473
        
        ' Q3: Clinician Subservience Risk Use Cases
        usecase "Expose Pixel-Level Activation Logic" as UC-25637
        usecase "Isolate Visual Noise/Artifacts" as UC-60739
        usecase "Commit Validated Ground-Truth Record" as UC-62864
        
        ' Q4: Double Blind Failure Use Cases
        usecase "Activate Clinical Investigation Mode" as UC-35956
        usecase "Execute Structured Morphology Annotation" as UC-47796
        usecase "Serialize Session to Telemetry Queue" as UC-01580
    }
}

' Human-System Interactions
Rad --> UC-48376
Rad --> UC-47988
Rad --> UC-92006

' Q2, Q3 & Q4 Interaction Entrypoints
Rad --> UC-55146 : Argue observations
Rad --> UC-60739 : Tag artifacts
Rad --> UC-47796 : Document manual findings

' Machine-to-Machine Pipelines
Grader --> UC-48376 : Feeds vision tensors & initial scores

' Internal Use Case Associations & Extends
UC-48376 ..> UC-25776 : <<include>>
UC-25776 ..> UC-02423 : <<include>>

' Q2 Loop Connections
UC-47988 <.. UC-22159 : <<extend>> (If clinician friction detected)
UC-22159 ..> UC-55146 : <<include>>
UC-55146 ..> UC-74821 : <<include>>
UC-74821 ..> UC-65473 : <<extend>> (If impasse or semantic drift caught)

' Q3 Loop Connections
UC-47988 <.. UC-25637 : <<extend>> (If clinician contests AI score)
UC-25637 ..> UC-60739 : <<include>>
UC-60739 ..> UC-62864 : <<include>>

' Q4 Loop Connections
UC-47988 <.. UC-35956 : <<extend>> (If low confidence & empty RAG)
UC-35956 ..> UC-47796 : <<include>>
UC-47796 ..> UC-01580 : <<include>>

' Final Hand-off Synchronization
UC-92006 ..> EMR : Sync standardized structural JSON data
@enduml

```

---

## 5. Blueprint Cross-Traceability Matrices

### 5.1 Scenario-to-Agent Mapping Tracking Matrix

This structural trace links the user behavior scenarios directly back to the active internal validation elements processing the loop.

```
+---------------------------+-----------------------+-------------------------+-------------------------+
| Interaction Scenario      | Core Vision Component | Dialogue Safety Layer   | Arbitration Safety Node |
+---------------------------+-----------------------+-------------------------+-------------------------+
| Q1: True Agreement        | VKIST Vision Grader   | LLM Explainer (CoT Log) | RAG-Referee (Clear)     |
| Q2: Automation Override   | VKIST Vision Grader   | Socratic Circuit Breaker| RAG-Referee (Active)    |
| Q3: Clinician Subservience| Feature Map Vis       | Objective Critic Dialog | RAG-Referee (Active)    |
| Q4: Double Blind Edge Case| Anomaly State Ingest  | Exploratory Morphology  | Telemetry Retrain Queue |
+---------------------------+-----------------------+-------------------------+-------------------------+

```

### 5.2 Functional Requirements Validation Trace

* **ULTS-FR-25 Criteria Trace 01:** The system must process initial classifications using pixel-percentage markers. Checked by: `UC-48376` $\rightarrow$ `UC-47988`.
* **ULTS-FR-25 Criteria Trace 02:** System designs must enforce a circuit breaker step if user actions indicate diagnostic mismatch or context drift. Checked by: `UC-22159` $\rightarrow$ `UC-74821`.
* **ULTS-FR-25 Criteria Trace 03:** Sessions documenting unmapped anatomical variants must bypass standard hospital charts and stream records directly to optimization sinks. Checked by: `UC-35956` $\rightarrow$ `UC-01580`.

---

## 6. Downstream UIX & Specification Target Anchors

This baseline file establishes structural anchor configurations for subsequent product development phases:

1. **Phase 4 (Workspace Dashboard Wireframing):** Wireframe templates must reserve split-screen display blocks: one side hosting the medical canvas with artifact isolation tools (`UC-60739`), and an inline section mapping socratic messaging interactions (`UC-55146`).
2. **Use Case Specification Drafting:** Individual use case descriptions can reference this anchor block to maintain absolute consistency regarding precondition bounds, primary exception vectors, and hand-off synchronization parameters (`EMR`).

---

*This engineering reference document accurately captures the system boundaries finalized during the requirement discovery sprint.*