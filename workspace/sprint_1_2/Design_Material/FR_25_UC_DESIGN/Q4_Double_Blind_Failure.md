# Q4: Double Blind Failure dues to edge-case
(AI Faulty / Doctor Biased)

Layered Three-Tier ML Stack Performance Impact (Your Proposed Design): Anomaly Escalation Protocol: In instances where both the diagnostic system and the clinician encounter an edge-case—or "unknown-unknown"—that lacks precedent in the current RAG knowledge base, the system initiates the Anomaly Escalation Protocol. The LLM Explainer detects this "epistemic uncertainty" (via low vision-stack confidence and empty RAG retrieval results) and shifts the interface from "Diagnostic Support" to "Clinical Investigation Mode." Instead of attempting to force a Grade-based diagnosis, the Internal Consultor guides the clinician to document the unique morphological features through a structured annotation protocol, facilitating a Socratic investigation into the anomaly. The system transparently acknowledges the limitation, explicitly stating that current clinical guidelines do not cover this specific presentation, and prompts the clinician to manually document findings. With the clinician’s consent, the workspace commits this session as a "Novel Research Case," automatically serializing the raw imaging tensors, clinician observations, and artifact logs to a secure telemetry queue, flagging the data for system maintainers to perform targeted model retraining and protocol refinement.

```planuml
@startuml
' Layout optimizations to secure compact rendering and prevent image fragmentation
skinparam linetype polyline
skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor #fefefe
    BorderColor #555555
}

' Actors strictly mapped to match your canonical architectural definitions
actor "Radiologist (UP5)" as Rad
actor "Internal Consultor (LLM Chat)" as Cons <<System>>
actor "System Maintainer" as Maint <<System>>

rectangle "VKIST MSK Workspace - Q4 Architecture" {
    
    usecase "Evaluate Epistemic Uncertainty Gate" as UC4_Trigger
    
    rectangle "Socratic Workspace UI Panel" {
        usecase "Shift to Clinical Investigation Mode" as UC4_Halt
        usecase "Engage in Socratic Discussion" as UC4_Socratic
        usecase "Render Manual Checklist Canvas" as UC4_Synth
    }
    
    rectangle "Verification & Arbitration Kernel" {
        usecase "Audit Chat Token Drift (BERT)" as UC4_BERT
        usecase "Execute RAG-Referee Check" as UC4_Referee
        usecase "Return Null-Match Signal" as UC4_RAG_Fetch
    }
    
    rectangle "Clinical Resolution Gate" {
        usecase "Document Novel Morphological Features" as UC4_Review
        usecase "Authorize Serialized Anomaly Package" as UC4_Finalize
    }
    
    usecase "Asynchronous Telemetry Queue Sync" as UC4_Sync
}

' Initial Data Intake and Uncertainty Routing Paths
Rad --> UC4_Trigger : Feed OOD Image Tensors
UC4_Trigger ..> UC4_RAG_Fetch : <<include>> (Triggers Empty Vector Result)
UC4_RAG_Fetch ..> UC4_Halt : <<extend>> (On Zero-Match Guidelines + Low Conf Tensors)
UC4_Halt ..> UC4_Synth : <<include>>

' Direct Socratic Analysis Run-time Workspace
Rad --> UC4_Socratic
Cons --> UC4_Socratic : Drive Exploratory Morphology Dialogue

' Live Guardrail and Exception Evaluation Paths
UC4_Socratic ..> UC4_BERT : Stream Conversation Tokens
UC4_BERT ..> UC4_Referee : <<include>> (Validates Logical Framing Stability)

' Manual Audit, Documenting Anomaly and Consent Finalization
Rad --> UC4_Review : Acknowledge Guideline Limitation
Rad --> UC4_Finalize : Provide Native Opt-In Telemetry Consent

' Async Data Serialization Sink to System Maintainer Ledger
UC4_Finalize ..> UC4_Sync : <<include>>
UC4_Sync --> Maint : POST Encrypted Tensors & Logs for Model Retraining
@enduml
```

![image.png](Q4%20Double%20Blind%20Failure%20dues%20to%20edge-case%20(AI%20Faul/image.png)