
### Insight-Note - @Đạt Trần Tiến (Daves Tran)

→ Additionally we shall develop the app follow this manner: PWA - progressive web app

- UP-6 insight (suggest the insight for converting toward FRs)
    - Insight - to FR-draft 1
        - Core Insight 1: The Information Bottleneck
            - Formulated Pain Point
                - **User Vulnerability:** Vietnamese Physiotherapists struggle to accurately target internal tissue pathologies during physical therapy sessions.
                - **Root Cause:** Diagnosing medical doctors rarely or poorly pass digital DICOM imaging streams down the operational chain, providing only brief, low-context paper or text-based prescription sheets.
                - **Negative Impact:** Clinicians are forced to execute high-intensity therapeutic modalities semi-blindly over estimated surface anatomy, drastically reducing treatment precision and patient efficacy.
            - Target Structural Keywords
                - `{information-clarification & context clarification}`
                - `{from the prescribe → detect where to treat}`
            - Functional Requirements Blueprint
                - **The Ingestion & Context Clarification Pipeline:** The platform must feature an integrated Optical Character Recognition (OCR) scanner tool optimized for mobile tablet arrays. When a PT receives a text-only sheet, the system scans the raw text, extracts localized shorthand clinical terms, and cross-references them with centralized clinical guidelines to generate immediate context clarification regarding structural contraindications.
                - **Automated Spatial Target Generation ("Prescribe  → Guide on Detect the Region of Treatment"):**
                    - Your database architecture must map abstract text instructions to specific coordinate layers. When a text prescription is parsed (e.g., *"Ultrasound therapy, left shoulder"*), the system can:
                        - automatically triggers a default, rotatable 3D musculoskeletal target field, highlighting the structural depth and biological tissue boundaries where the treatment must physically occur.
                        - Generating suggestion guidance on how to interpret the prescrbe under PT knowledge-base + suggest the certain treatment methodology for referential value
        - Core Insight 2: The Cross-Domain Literacy Gap
            - Formulated Pain Point
                - **User Vulnerability:** Vietnamese Physiotherapists struggle to accurately interpret raw diagnostic findings and seamlessly coordinate with prescribing medical specialists.
                - **Root Cause:** Their foundational training is rooted entirely in kinetic biomechanics, which completely mismatches the physician’s world of complex radiological pixel data. This structural literacy gap is severely compounded by a massive 84% foreign language deficit and zero academic background in evaluating clinical statistics or research methodologies.
                - **Negative Impact:** The communication mismatch creates high inter-departmental silos, forces a reliance on subjective clinical guesswork, and increases the risk of deploying highly ineffective or contraindicated treatment tracks.
            - Target Structural Keywords
                - `{Cross-Domain Knowledge Translator Between Clinicians & Specialist}`
                - `{Educating Channel / Communication medium}`
            - **Functional Requirements Blueprint**
                - **Cross-Domain Knowledge Translation Canvas:** Your frontend rendering engine must not display a raw, uninterpreted grayscale DICOM viewport. The system must feature a visual abstraction layer that automatically translates multi-slice pixel matrices and annotations into an interactive 3D musculoskeletal medium. Complex radiological data points are remapped into intuitive anatomical indicators (e.g., muscle layer depth maps, color-coded inflammation zones) that line up natively with the PT's biomechanical domain knowledge.
                - **Asynchronous Bidirectional Communication Medium:** Because local medical regulations strictly bar technicians from editing primary physician diagnosis records, the collaborative workspace must provide an isolated "Clinical Observation & Progress Flagging" backchannel. The PT interacts with the workspace by pinning tactile assessment data directly onto the shared 3D scan canvas, which compiles an objective, standardized data summary that can be pushed seamlessly to the physician's review dashboard.
                - **The Visual Patient-Educating Channel:** To address the locomotive health education requirement, the workspace must feature a decoupled "Patient View" mode switch. This toggle filters out dense clinical indicators and transforms the active 3D biomechanical model into a simplified, clear educational medium. The therapist utilizes this channel to visually demonstrate joint mechanics and injury zones directly to the patient, replacing blind compliance with objective spatial understanding.
            
            ### 
            
    - **Insight to FR draft 2**
        
        To ensure our engineering team does not waste resources rebuilding duplicate features, we need to carefully cross-reference this **Physiotherapist (PT) Blueprint** with our previous **Rheumatologist & Orthopedic Surgeon Workspace (UP-7)**.
        
        Below is a structural overlap analysis, followed by the refined, non-overlapping Functional Requirements written strictly from the PT’s unique clinical point of view.
        
        #### Part 1: Overlap & Delta Analysis (UP-7 vs. PT Workspace)
        
        Our primary goal is to ensure the PT requirements capture **functional differences**, not just terminology differences.
        
        ### 🏢 What is Overlapped (Shared Infrastructure)
        
        - **The Asynchronous Communication Medium vs. UP-7 FR-02 (Voice Memo/JSON Timeline):** Both requirements solve the same technical problem: asynchronous communication via metadata layers over a shared canvas. They should be unified into a single backend thread module.
        - **The Visual Patient-Educating Channel vs. UP-7 FR-04 & FR-05 (Adaptive 3D & Sandbox Link):** The code needed to switch to a simplified 3D viewport or hand over a view to a patient is identical to the underlying architecture we designed for the doctor's profile.
        
        ### ⚡ What is Unique to the PT Context (The Real Deltas)
        
        - **Upstream Data Ingestion:** Doctors *create* the DICOM and write text prescriptions. PTs *receive* the raw text and have to parse it. The OCR ingestion pipeline is $100\%$ unique to the PT workflow.
        - **Text-to-3D Coordinate Projection:** Doctors map 2D DICOM coordinates to 3D. PTs need to map **abstract text descriptions** (e.g., *"Supraspinatus tendinitis"*) to 3D coordinates on a model when the raw DICOM is missing.
        - **Biomechanics vs. Radiology:** Doctors look for raw structural or inflammatory data. PTs look for kinematic impact (e.g., muscle depth layers, range-of-motion constraints, therapy execution depths).
        
        ### Part 2: Refined, Non-Overlapping PT Functional Requirements
        
        #### FR-PT-01: Client-Side WebML Prescription Parser (TensorFlow.js)
        
        - **PT Point of View:** "Patients walk in with a crumpled piece of text-based paper from the doctor. I need to instantly parse what treatment to give them without sending their medical notes to an insecure external cloud server."
        - **Technical & Demography Pivot:** Instead of heavy, costly cloud-based OCR APIs, this runs entirely in the mobile web browser. To keep sensitive health data strictly private under **Decree 13/2023/ND-CP**, no images leave the phone.
        - **Functional Scope:**
            - The PWA (progressive web-app) must use a lightweight, browser-optimized `MobileNetV2` text-segmentation model via TensorFlow.js to scan text via the phone's native camera stream (`getUserMedia`).
            - The script must parse Vietnamese localized shorthand clinical terms directly on-device to extract the targeted joint zone, prescribed therapy modality (e.g., Ultrasound, Shockwave), and frequency.
            - **Instant Safety Warning:** The client-side logic immediately processes the extracted words against a lightweight dictionary to trigger a prominent warning panel if any structural contraindications exist (e.g., severe osteoporosis warnings for manual manipulation).
        
        #### FR-PT-02: Zero-GPU Text-to-3D Target Mapping Framework
        
        - **PT Point of View:** "When the doctor provides zero digital X-ray files, I have to guess how deep the tissue pathology is based on their text notes. I need a clear visual guide on my phone, even if it's an old device."
        - **Technical & Demography Pivot:** Running a live, mathematically intense 3D translation matrix inside a mobile browser on a legacy, weak-GPU phone will drop frame rates and crash. We implement a **Hybrid Dual-Engine** directly in the PWA.
        - **Functional Scope:**
            - **High-Spec Profile (Three.js):** If the browser passes a WebGL capabilities test, the abstract text tokens parsed in FR-PT-01 are mapped to spatial coordinates on an interactive 3D bone/muscle model.
            - **Low-Spec Profile (CPU-Bound Sprite Animator):** If the device's GPU is flagged as outdated, the system halts Three.js execution. It fetches a pre-rendered 36-frame flat image sequence (a 360-degree turntable shot of the musculoskeletal target). The phone's CPU simply switches the index of the visible 2D image based on the PT's swipe gestures, creating a zero-GPU "3D rotation" effect.
            - The system dynamically draws an SVG vector shape highlight over the target area to indicate precisely which tissue layer depth (superficial skin vs. deep muscle belly) the therapy must focus on.
        
        #### FR-PT-03: Biomechanical Kinetic Overlay & Muscle Depth Mapping
        
        - **PT Point of View:** "Doctors care about bone structural alignment. I care about the kinetic soft-tissue layers, muscle fibers, and where exactly to place my physical therapy machine probes."
        - **Technical & Demography Pivot:** Since we cannot use native OS GPU layers or native haptic engines in a standard PWA context, we rely on pure CSS layout composition to avoid interface lag.
        - **Functional Scope:**
            - The canvas view must provide a dedicated **Kinetic Overlay Toggle**. This maps a colorful, transparent cross-section depth map ($1\text{cm}$ to $5\text{cm}$ color coding) directly over the target treatment region.
            - Rather than relying on heavy WebGL shader calculations, the app dynamically appends lightweight, text-based HTML `<svg>` paths detailing muscle cross-sections on top of the base image viewport.
            - This allows the PT to visualize the estimated soft-tissue depth to calculate the correct angle of approach when placing ultrasound transducers or laser therapy devices on the patient's body.
        
        #### FR-PT-04: Isolated Data-Segregated Observation & Progress Tracking Track
        
        - **PT Point of View:** "Legally, I cannot change the primary doctor’s medical diagnosis. But as I work with the patient daily, I need to track their range-of-motion improvements and flag pain triggers that the doctor should see before their next follow-up."
        - **Technical & Demography Pivot:** To satisfy both local medical regulations and the strict access control requirements of **Decree 13/2023/ND-CP**, data tracks must be isolated.
        - **Functional Scope:**
            - The system implements strict role-based data encapsulation. The PT frontend interface operates on a **Read-Only** schema regarding the doctor's primary diagnostic charts or annotations.
            - The PWA provides a distinct **Kinetic Tracking Channel**. The PT can tap the screen to place "Kinetic Progress Pins" onto a separate workspace layer.
            - Each pin logs localized, chronological metrics: Range of Motion (ROM) angles, subjective pain indices ($1\text{--}10$), and local tissue behavior notes. This timeline sub-packet is serialized as text data and pushed directly to the physician's tracking panel without mutating the primary medical file.
        
        #### FR-PT-05: DOM-Mirrored Kinetic Demonstration (Patient Education Mode)
        
        - **PT Point of View:** "When doing manual therapy, poor patients often resist or tense up because they don't understand their joint mechanics. I need to show them exactly why they are hurting using their own legacy phones, without the app stuttering."
        - **Technical & Demography Pivot:** Emulating dynamic bone impingements in real-time WebGL on a patient's low-end phone causes extreme overheating. We move the animation burden from the GPU to simple DOM manipulation.
        - **Functional Scope:**
            - The PWA features a dedicated "Patient Demonstration Mode" with a clean, low-density layout interface.
            - The view presents a split layout: a static anatomical image on one side, and a simple html Range-of-Motion slider on the other.
            - As the PT moves the slider to match the patient’s physical arm or leg position, the app cycles through a lightweight array of cached 2D illustrations. This visual progression dynamically demonstrates joint flexion and extension, color-coding the exact soft tissues that are tightening or impinging. This gives the patient an immediate visual understanding of their pain using $0\%$ GPU processing power.
        
        #### Low-Cost PWA Technical Architecture Overview
        
        ![Screenshot 2026-06-04 at 09.30.46.png](User-Research%20Result/Screenshot_2026-06-04_at_09.30.46.png)
        
        #### Engineering Architecture Stack for MVP:
        
        - **Frontend Core:** React.js configured as an installable PWA with a robust Service Worker for aggressive caching, optimizing performance for patchy hospital Wi-Fi networks.
        - **Data Encryption:** WebCrypto API on the client side to securely wrap sensitive patient details before syncing with a local Vietnamese host (e.g., Viettel IDC) to ensure compliance with Decree 13.
        - **Graphics Delivery:** Hybrid WebGL-to-DOM rendering logic, ensuring that poor patients with legacy CPU-strong/GPU-weak phones receive the exact same educational data via lightweight 2D frame-switching.
        
- UP-7 insight (suggest the insight for converting toward FRs)
    - Some keywords & insight on **Rheumatologist & Orthopedic Surgeon** from the user-profile
        - Who they are: senior specialist that `ultimate consumers of the diagnostic imaging data and the primary architects of the patient's comprehensive treatment plan.`  → they are the must character in the patient’s journey & patient shall have to interact with them & they shall interact with multiple patients
        - They have to work with multiple information on user’s profile & pathologies → synthesize to have a picture of patients & yeild the treatment journey & treatment strategy & handle the legal & ethical & patient’s safetiness & outcome
        - Understand the clinical implication + patient’s psychology + ready to explain & spend-time to explain with patient & debunk misinformation - but while they still have tight-time constrain
        - They may not known surely what patient’s are doing before reach toward them → harder to form the patient’s pathologies and harder to form diagnosing-picture & put them under a broken interaction & challenging case where patient may come with compilcations that exacerbating the conditions
        - They less-interest in shallow ML algorithm for identify the fracture where they can do , but interest more on consultative & deep  while fast analysis & predictive (like explain the root-cause & the pathologies pattern & the potential adjustment - covering edge_case of miss-diagnosing)
        - They also interest with `a massive potential force multiplier for patient education, provided it **visually translates complex DICOM data into beautifully simple formats the patient can instantly understand**, thereby saving precious consultation minutes for more personalized discussion on treatment plan. (while doctors are assure the model are faithful & accurate)`
        - These clincians `need the platform to automatically aggregate highly fragmented patient data (historical X-rays, recent MRIs, scattered lab results) into a single, unified, rapid-consumption dashboard to exponentially expedite their clinical decision-making process.`
    - From Insight toward FR
        
        #### FR-01: Haptic-Assisted Touch Viewport & Edge-Snapping Magnifier
        
        - **User Insight:** Rheumatologists and Orthopedic Surgeons require pixel-level accuracy to calculate structural joint metrics (e.g., Cobb angles, joint space narrowing). On a compact 6-inch mobile screen, human fingers naturally obscure these fine anatomical landmarks.
        - **Engineering Feasibility:** High (9/10). Utilizes native iOS/Android low-latency graphics canvas and built-in vibration APIs.
        - **Functional Scope:**
            - **Touch Viewport:** Renders a single DICOM viewport optimized for native multi-touch gestures (pinch-to-zoom, two-finger pan, single-finger window/level adjustments).
            - **Floating Lens:** Activating an annotation tool and pressing down must trigger a floating, high-magnification "lens" widget positioned $150\text{px}$ vertically above the touch point to bypass finger obstruction.
            - **Edge-Snapping:** Incorporates a lightweight, client-side edge-detection algorithm (Canny/Hough transform). When drawing, the crosshairs automatically snap to the nearest high-contrast bone boundary, confirmed by a localized native haptic pulse.
        
        #### FR-02: Asynchronous Voice-Over Annotation & Timeline Canvas
        
        - **User Insight:** Clinicians navigate highly fragmented, fast-paced hospital rounds and surgical schedules in Vietnamese facilities. Coordinating live, simultaneous multi-user phone calls is functionally unfeasible, yet basic text messaging lacks spatial anatomical context.
        - **Engineering Feasibility:** High (8/10). Replaces complex real-time WebSockets with an offline-first, asynchronous data synchronization model suited for patchy hospital Wi-Fi networks.
        - **Functional Scope:**
            - **Metadata Recorder:** Captures microphone input while recording all viewport coordinate state changes ($X, Y$ positions, zoom vectors, panning arrays, and hand-drawn vectors) instead of recording a heavy video file.
            - **Interactive Playback:** Compiles these telemetry inputs into a serialized JSON timeline file. When the receiving doctor opens the case memo, the app replays the sender’s exact viewport transformations and vector drawing steps synchronized with the audio track.
            - **Threaded Replays:** Supports nested, asynchronous audio/canvas replies directly inside the specific case file workspace.
        
        #### FR-03: Progressive Disclosure Sheets & Native Workflow Alerts
        
        - **User Insight:** Displaying automated medical guidelines (e.g., Kellgren-Lawrence grading profiles) alongside a high-fidelity image on a mobile screen causes severe cognitive overload.
        - **Engineering Feasibility:** High (9/10). Uses highly optimized, native OS interface layouts and lightweight push services (FCM/APNS) that run efficiently on both flagship and mid-tier Android devices.
        - **Functional Scope:**
            - **Single-Focus Layout:** Dedicates $100\%$ of the background viewport strictly to the active DICOM canvas.
            - **Progressive Bottom-Sheet:** Confines automated clinical telemetry, AI-driven objective calculations, and reference guidelines within an expandable native Bottom-Sheet component. Supports three swipe states: $25\%$ peek view, $60\%$ detailed data view, and $100\%$ full-screen deep dive.
            - **Deep-Linked Push Notifications:** Triggers a native OS push alert when a case update occurs, deep-linking the receiving doctor directly into the specific case viewport configuration state.
        
        #### FR-04: Hardware-Adaptive 3D Musculoskeletal Synchronization Engine
        
        - **User Insight:** Patients struggle to interpret abstract 2D X-ray slices, which directly hinders their locomotive health literacy. The platform must connect 2D pathologies to an intuitive 3D visualization without crashing the devices of low-income or rural patients utilizing legacy phone chipsets.
        - **Engineering Feasibility:** High (8/10). Dual-Engine Framework. The system executes a client-side feature detection script probing WebGL and GPU vendor extensions (filtering out low-end units like Mali-T, Adreno 3xx, or PowerVR Rogue architectures).
        - **Functional Scope:**
            - **Profile A (High-Performance WebGL Engine):** Maps 2D DICOM coordinates onto a standardized, lightweight 3D skeletal mesh running on an embedded cross-platform WebGL/Three.js engine. Tapping a pathology highlights the isolated 3D node in real time.
            - **Profile B (CPU-Bound Sprite-Sheet Fallback):** Bypasses WebGL entirely if weak GPU flags are triggered. The system downloads a pre-compiled, 36-frame turntable "sprite sheet" of the model (pre-rendered at  $10^\circ$  increments on the cloud backend). The client phone uses its stable CPU to index and switch the visible frame based on the patient's swipe gestures, creating a zero-GPU 3D rotation effect.
        
        #### FR-05: Sensitive Data Sandbox & Patient Share Portal (Decree 13/2023/ND-CP Compliant)
        
        - **User Insight:** Patients need clean, accessible, jargon-free medical information on their personal devices post-consultation without dealing with complex medical document readers or risking leakages of their sensitive health histories.
        - **Engineering Feasibility:** Moderate (8/10). Strictly aligned with **Vietnam's Decree 13/2023/ND-CP** requirements for processing sensitive personal data (health status and clinical records).
        - **Functional Scope:**
            - **Explicit Consent Check:** The portal cannot render or process the patient packet until a native, explicit "Opt-In Consent" click-action is logged and cryptographically recorded from the patient, conforming to Decree 13 legal consent parameters.
            - **Data Sanitization & Server-Side Flattening:** Strips away raw DICOM arrays, institutional metadata, and backend telemetry. If a `LOW_GPU` profile is active, the local cloud server flattens all clinician vector overlays directly into a compressed static JPEG to offload rendering tasks from weak patient browsers.
            - **Decentralized Local AES-256 Encryption:** In accordance with Decree 13 mandates for technical protection measures, the app must encrypt the patient's packet using localized AES-256 bit keys.
            - **Time-Expiring Tokenized Access:** Generates a unique QR code or deep link mapped to a one-time token with a $14\text{-day}$ Time-To-Live (TTL). When scanned over standard local 4G, it loads an adaptive dashboard in $\le 2.0\text{ seconds}$ hosting only the simplified locomotive health summaries and clinician voice memos.
        
        ### Updated Technical Blueprint & Architecture Summary
        
        ![Screenshot 2026-06-04 at 09.31.42.png](User-Research%20Result/Screenshot_2026-06-04_at_09.31.42.png)
        
        ### Updated Recommended Target MVP Tech Stack
        
        - **Cross-Platform Interface:** Flutter (Dart) or React Native (TypeScript) to optimize code reusability across Vietnam's divided OS market.
        - **DICOM Framework:** OFFIS DCMTK compiled to native C++ mobile binaries via platform channels.
        - **3D & Hybrid Visualization Subsystem:** An inline WebView context using vanilla JavaScript. The script evaluates graphics-pipe telemetry and dynamically switches rendering branches between Three.js (WebGL) and optimized CSS/DOM-level image switching (Sprite-Sheet).
        - **Data Compliance Module:** Client-side encryption using localized cryptographic plugins. All production cloud infrastructure, file caches, and backend web databases must be hosted on local cloud server providers (e.g., Viettel IDC, VNPT, or local AWS/GCP regions) to fully satisfy local data protection audit requirements under Decree 13.