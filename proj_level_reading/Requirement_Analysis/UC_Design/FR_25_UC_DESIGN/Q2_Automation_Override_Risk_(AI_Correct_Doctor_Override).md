# Q2: Automation Override Risk
(AI Correct / Doctor Oversights / Confuse)

Layered Three-Tier ML Stack Performance Impact (Your Proposed Design): The Conversational Circuit Breaker triggers when a clinician disagrees / confuse / uncertain with the system's diagnostic grade, halting the workflow to launch an interactive Socratic dialogue that bridges the gap between human intuition and machine inference. In this mode, the system (LLM-explainer) shall synthesize raw VKIST-ML vision tensors, GradCAM activation heatmaps, and evidence retrieved via RAG into a collaborative analysis session, forcing the clinician to articulate their reasoning against the machine's spatial and vascular observations. To ensure diagnostic integrity, a BERT-based hallucination detector continuously monitors the chat for semantic drift or illogical premises; if the conversation reaches an impasse or the system detects potential contextual hallucination, the RAG-Referee intervenes as an unbiased arbiter. This referee bypasses the conversational history to provide definitive, evidence-based source material from clinical guidelines (such as ESSR) directly tied to the raw imaging metrics, resolving the ambiguity through objective, verifiable medical evidence rather than subjective negotiation.

```jsx
@startuml
skinparam linetype polyline
skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor #fefefe
    BorderColor #555555
}

' Actors
actor "Radiologist (UP5)" as Rad
actor "Internal Consultor (LLM Chat)" as Cons <<System>>
actor "Hospital EMR" as EMR <<System>>

rectangle "VKIST MSK Workspace - Q2 Architecture" {
    
    usecase "Trigger Circuit Breaker Panel" as UC2_Trigger
    
    rectangle "Socratic Workspace UI Panel" {
        usecase "Lock Main Diagnostic Flow" as UC2_Halt
        usecase "Engage in Socratic Discussion" as UC2_Socratic
        usecase "Display Visual GradCAM Overlay" as UC2_Synth
    }
    
    rectangle "Verification & Arbitration Kernel" {
        usecase "Audit Chat Token Drift (BERT)" as UC2_BERT
        usecase "Execute RAG-Referee Check" as UC2_Referee
        usecase "Query Immutable Guideline Base" as UC2_RAG_Fetch
    }
    
    rectangle "Clinical Resolution Gate" {
        usecase "Review Referee Verdict Card" as UC2_Review
        usecase "Commit Signed Diagnosis" as UC2_Finalize
    }
    
    usecase "EMR Ledger Sync" as UC2_Sync
}

' Core Interaction Flow
Rad --> UC2_Trigger : Disagreement/Uncertainty
UC2_Trigger ..> UC2_Halt : <<include>>
UC2_Halt ..> UC2_Synth : <<include>>

' Dynamic Chat Loop between Doctor and Internal Consultor LLM
Rad --> UC2_Socratic
Cons --> UC2_Socratic : Drive Pathologic Inquiry Dialogue

' Asynchronous Automated Verification Channel
UC2_Socratic ..> UC2_BERT : Stream Conversation Tokens
UC2_BERT ..> UC2_Referee : <<extend>> (Triggered on Impasse / Chat Hallucination)
UC2_Referee ..> UC2_RAG_Fetch : <<include>>
UC2_RAG_Fetch ..> UC2_Review : Inject Ground-Truth Evidence

' Finalization Steps
Rad --> UC2_Review
Rad --> UC2_Finalize
UC2_Finalize ..> UC2_Sync : <<include>>
UC2_Sync --> EMR : POST Validated JSON Payload
@enduml
```

![image.png](Q2%20Automation%20Override%20Risk%20(AI%20Correct%20Doctor%20Ove/image.png)