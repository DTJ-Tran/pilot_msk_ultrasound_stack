# CONTEXT.md for the Usecase Discovery : FR-25

- The requirement: FR-25 == ULTS-Đánh giá và phân cấp mức độ viêm màng hoạt dịch (Synovitis Grading)

- Explain why the se should care on this usecase in the design process
    - **The Gap:** Lợi ích kỹ thuật & Giá trị cốt lõi của Use Case Phân cấp Viêm màng hoạt dịch đối với Kiến trúc Phần mềm (Missing Clinical rationale vs. Engineering value optimization for Synovitis Grading).
    - **The Question:** Tại sao quy trình lâm sàng chuẩn hóa này lại đảm bảo tính chính xác khi phân cấp (`Synovitis Grading`) và tại sao một Kỹ sư Phần mềm (SE) phải đặc biệt quan tâm đến Use Case này khi thiết kế sản phẩm?
    - **The Hint:** Để xây dựng một sản phẩm Y tế (Healthcare AI Product) thành công, chúng ta không được coi Use Case này chỉ là một tính năng CRUD hay hiển thị ảnh đơn thuần. Hiểu rõ bản chất toán học/vật lý của quy trình giúp SE thiết kế cơ chế lưu trữ dữ liệu (Data Schema), cấu hình Pipeline xử lý ảnh AI và tối ưu hóa trải nghiệm UIX không bị lỗi logic giải phẫu.
    - **The Recommendations:** Dưới đây là câu trả lời phân tích sâu dưới góc nhìn của một Kỹ sư Hệ thống / Lập trình viên:
    
    ### PHẦN 1: Tại sao quy trình này đảm bảo việc phát hiện và phân cấp chính xác? (Góc nhìn Data Pipeline & Signal Processing)
    
    Nếu coi cơ thể người là một hệ thống phần cứng và máy siêu âm là một module quét dữ liệu ngoại vi (Hardware Scanner), quy trình 6 bước lâm sàng chính là các điều kiện tiền đề để **đảm bảo tính toàn vẹn của tín hiệu (Signal Integrity)** và ngăn chặn **nhiễu dữ liệu (Data Corruption)**:
    
    1. **Khử nhiễu biên (Eliminating Boundary Noise - Bước 1):** việc gập đầu gối 20°–30° tương đương với việc thực hiện lệnh `Format / Standardize` bề mặt quét. Nó triệt tiêu hiện tượng *Bất đẳng hướng âm học (Acoustic Anisotropy)* – vốn là một dạng nhiễu tín hiệu vật lý khiến mô khỏe mạnh bị biến đổi thành các pixel đen giả lập tổn thương.
    2. **Cố định Hệ tọa độ (Fixing Coordinate System - Bước 2):** Đặt đầu dò dọc (`Longitudinal`) giúp mô hình AI thu được một contract dữ liệu ảnh tĩnh có cấu trúc giải phẫu phân tầng rõ ràng (`Multi-layered Frame`). Đỉnh xương bánh chè hoạt động như một điểm mốc $X, Y = (0,0)$ cố định để hệ thống chạy Edge Detection chuẩn xác.
    3. **Phân tích Đa luồng song song (Multi-threading Analytics - Bước 3 & 4):**
        - **Luồng B-Mode (Cấu trúc Hình học):** Trích xuất độ dày mô (`float thickness_mm`) $\rightarrow$ Phản ánh dung lượng thiệt hại vật lý tĩnh (Structural Damage).
        - **Luồng Power Doppler (Lưu lượng Biến động):** Trích xuất mật độ màu của dòng máu (`float vascular_percentage`) $\rightarrow$ Phản ánh lưu lượng dữ liệu thời gian thực đang chạy (Active Inflammation).
    4. **Tránh lỗi nén hệ thống (Avoiding Signal Throttling):** Việc lướt nhẹ tay đầu dò (minimal pressure) giữ cho luồng truyền dẫn tín hiệu mạch máu không bị bóp nghẹt (Throttling), tránh việc hệ thống tính toán sai lệch điểm số hoạt tử/viêm mạch dẫn đến kết quả âm tính giả.
    
    ### PHẦN 2: Tại sao Kỹ sư Phần mềm (SE) phải đặc biệt quan tâm đến Use Case này?
    
    Từ góc nhìn sản phẩm và kiến trúc hệ thống của dự án `VKIST_ULTRASOUND`, đây không phải là một tính năng bổ sung, mà chính là **Core Core Business Logic (Lõi nghiệp vụ quyết định)** vì các lý do sau:
    
    ### 1. Định hình Data Model (Schema) cho toàn bộ hệ thống
    
    Nếu không hiểu quy trình này, bạn sẽ thiết kế cơ sở dữ liệu bị thiếu trường dữ liệu nghiêm trọng. Điểm số `Synovitis Grade` không thể lưu dưới dạng một trường `int grade` đơn giản. Dữ liệu y khoa chuẩn hóa bắt buộc phải là một đối tượng phức hợp (Compound Object Model):
    
    JSON
    
    ```
    {
      "patient_id": "BN-10023",
      "scan_metadata": {
        "joint": "KNEE",
        "side": "RIGHT",
        "plane": "suprapat-long",
        "patient_flexion_degree": 25
      },
      "extracted_metrics": {
        "synovial_thickness_mm": 4.2,
        "power_doppler_area_percentage": 34.5
      },
      "severity_classification": {
        "suggested_grade": 2,
        "confirmed_grade": 2,
        "is_overridden_by_doctor": false
      }
    }
    ```
    
    ### 2. Kích hoạt State Machine & Pipeline xử lý của AI (Mô tả trong tài liệu VKIST)
    
    Theo tài liệu kiến trúc của hệ thống, Use Case này là điểm kết thúc (`Final Destination`) của một Pipeline phân nhánh phức tạp. Khi ảnh DICOM/Siêu âm được đẩy lên hệ thống:
    
    - **Mô hình 1 (ConvNeXt):** Kiểm tra góc chụp. Nếu và chỉ nếu kết quả trả về đúng `sup_up_long`, hệ thống mới kích hoạt State tiếp theo.
    - **Mô hình 2 (EfficientNet/MedViT):** Kiểm tra trạng thái phân loại nhị phân `Has Inflammation = True/False`.
    - **Mô hình 3 (MedSAM/UNet):** Tiến hành phân đoạn vùng ảnh (Segmentation) tạo Mask đè màu để tính toán diện tích pixel bị tổn thương, từ đó tự động map ra điểm số Phân cấp từ 0 đến 3.
        
        Nếu Use Case này bị lỗi hoặc UIX thiết kế không khớp, toàn bộ Pipeline AI trị giá hàng nghìn giờ huấn luyện phía sau sẽ mất hoàn toàn giá trị sử dụng thực tế.
        
    
    ### 3. Giải quyết bài toán Tải trọng hệ thống và Kiệt sức lâm sàng (Clinical Exhaustion)
    
    Tại các bệnh viện công tuyến trung ương của Việt Nam (Bạch Mai, Bệnh viện E), một bác sĩ (UP5) phải xử lý >100 ca/ca trực.
    
    - Nếu không có phần mềm: Bác sĩ phải đổi ghế, chuyển ứng dụng, gõ tay kết quả vào hệ thống EMR thủ công $\rightarrow$ Nút thắt cổ chai gây delay hệ thống (Latency).
    - Khi có Use Case này được tự động hóa trên Dashboard: AI tính toán diện tích, trả về gợi ý bậc viêm ngay trên canvas xem ảnh, bác sĩ chỉ mất đúng 1 click chuột để xác nhận và Sync tự động sang Database tổng. Bạn đang giúp bệnh viện giảm thời gian xử lý một ca từ 5 phút xuống còn 30 giây, trực tiếp tối ưu hóa thông lượng (Throughput) cho toàn bộ hạ tầng y tế.
    - **The Alignment Check:** Với góc nhìn bóc tách hệ thống và phân tích Pipeline tín hiệu/AI như trên, bạn đã thấy rõ được bài toán kiến trúc mình cần giải quyết ở Use Case này chưa, hay có điểm nào cần làm sáng tỏ thêm trước khi chúng ta vẽ sơ đồ Use Case bằng PlantUML?
- Explain Why doctor are caring so much on this usecase
    - **The Gap:** Hiểu rõ động lực lâm sàng và giá trị chẩn đoán thực tế của Bác sĩ (Missing Clinical Drivers and Real-World Diagnostic Insights for Synovitis Grading).
    - **The Question:** Tại sao Bác sĩ Chẩn đoán hình ảnh (UP5) lại đặc biệt quan tâm đến Use Case Phân cấp Viêm màng hoạt dịch (`Synovitis Grading`), và chỉ số này tiết lộ điều gì cốt lõi trong hành trình chẩn đoán, điều trị của bệnh nhân?
    - **The Hint:** Trong y khoa, bản thân hình ảnh siêu âm xám chỉ là dữ liệu thô (raw data). Kết quả phân cấp từ Use Case này chính là **thông tin có cấu trúc (structured insights)** giúp bác sĩ trả lời câu hỏi cốt lõi của lâm sàng: Bệnh nhân này đang bị tàn phá khớp ở mức độ nào, tổn thương này là mạn tính (sẹo mô) hay cấp tính (đang bùng phát), và phác đồ điều trị bằng thuốc hoặc can thiệp ngoại khoa nào là chính xác nhất.
    - **The Recommendations:** Dưới đây là bóc tách chi tiết lý do vì sao bác sĩ cần Use Case này, được phân tích rõ ràng để một Kỹ sư Phần mềm nắm bắt trọn vẹn nghiệp vụ (Domain Knowledge):
    
    ### 1. Phân biệt Giữa "Tổn thương Cũ" (Mạn tính) và "Đợt Viêm Cấp" (Đang bùng phát)
    
    - **Ý nghĩa lâm sàng:** Khi nhìn vào ảnh siêu âm đen trắng (B-mode), bác sĩ thấy một vùng màng hoạt dịch dày lên (ví dụ: dày 4mm). Tuy nhiên, ảnh đen trắng đơn thuần **không thể** cho biết vùng phì đại đó là vết sẹo cũ từ 3 năm trước (mô xơ đã ổn định) hay là vùng mô đang liên tục sưng tấy, ăn mòn sụn khớp.
    - **Use Case tiết lộ điều gì:** Bằng cách kết hợp luồng dữ liệu của **Power Doppler**, Use Case này bóc tách và định lượng chính xác mật độ mạch máu tăng sinh (`Hypervascularity`).
        - *Dày mô + Không có tín hiệu Doppler (Grade 1):* Tổn thương cũ, chỉ cần theo dõi hoặc vật lý trị liệu.
        - *Dày mô + Tín hiệu Doppler dày đặc (Grade 3):* Ổ viêm đang hoạt động cực kỳ dữ dội. Hệ thống miễn dịch của bệnh nhân đang tấn công nhầm vào chính các tế bào khớp gối, giải phóng hàng loạt enzyme ăn mòn sụn và xương. Bác sĩ cần phải can thiệp ngay lập tức bằng thuốc ức chế miễn dịch mạnh (như Corticoid hoặc DMARDs) để chặn đứng dòng thác phá hủy này.
    
    ### 2. Điểm Số Quyết Định Phác Đồ Điều Trị (Actionable Clinical Metric)
    
    Điểm số Phân cấp từ 0 đến 3 không phải là một cái tag hiển thị cho đẹp, nó hoạt động giống như một **luồng điều hướng logic (Decision Tree)** quyết định trực tiếp hành động lâm sàng của bác sĩ:
    
    - **Grade 0 (Bình thường):** Chuyển bệnh nhân sang chế độ phòng ngừa, xuất viện.
    - **Grade 1 (Nhẹ):** Chỉ định điều trị nội khoa bảo tồn ở mức độ thấp (Dùng thuốc kháng viêm không Steroid - NSAIDs, thay đổi lối sống, tập vật lý trị liệu với bác sĩ PT - UP6).
    - **Grade 2 (Vừa):** Cân nhắc tiêm thuốc nội khớp (tiêm Corticoid trực tiếp vào ngách khớp gối để dập dịch viêm tại chỗ) kết hợp điều trị thuốc đặc hiệu.
    - **Grade 3 (Nặng/Nghiêm trọng):** Rút dịch khớp (Arthrocentesis) để giảm áp lực, chỉ định nhập viện điều trị tích cực, hoặc chuyển tuyến ngoại khoa để thực hiện phẫu thuật nội soi cắt màng hoạt dịch (Synovectomy) nhằm cứu lấy sụn khớp trước khi gối bị biến dạng hoàn toàn không thể phục hồi.
    
    ### 3. Thước Đo Khách Quan Để Đánh Giá Hiệu Quả Thuốc (Treatment Monitoring Dashboard)
    
    - **Nỗi đau của Bác sĩ:** Khi điều trị các bệnh tự miễn như Viêm khớp dạng thấp, bệnh nhân phải uống thuốc ròng rã nhiều tháng trời. Nếu bác sĩ chỉ hỏi bệnh nhân *"Bác có bớt đau không?"*, câu trả lời sẽ cực kỳ chủ quan và không chính xác (do ngưỡng chịu đau của mỗi người khác nhau và có hiệu ứng giả dược).
    - **Use Case tiết lộ điều gì:** Use Case này cung cấp một **Standardized Baseline (Mốc chuẩn hóa)** để so sánh liên tục qua các mốc thời gian (Time-series Analysis).
        - *Tháng 1:* Bệnh nhân đến khám $\rightarrow$ Hệ thống chấm **Grade 3** (Màng hoạt dịch dày 6mm, Doppler phủ 65% area).
        - *Tháng 3 (Sau 2 tháng uống thuốc):* Bệnh nhân tái khám $\rightarrow$ Hệ thống chấm **Grade 1** (Màng hoạt dịch giảm còn 2.5mm, Doppler chỉ còn vài chấm cô lập).
            
            $\rightarrow$ Phần mềm tiết lộ cho bác sĩ một bằng chứng số liệu toán học tuyệt đối: **Phác đồ thuốc hiện tại đang hoạt động hiệu quả**, tiếp tục duy trì liều lượng. Ngược lại, nếu điểm số vẫn là Grade 3, hệ thống cảnh báo bác sĩ rằng bệnh nhân đang kháng thuốc, phải đổi sang loại thuốc sinh học đắt tiền hơn ngay lập tức.
            
    
    ### 4. Triệt Tiêu Biến Thiên Giữa Các Bác Sĩ (Eradicating Inter-observer Variability)
    
    - **Thực trạng tại bệnh viện:** Việc phân cấp siêu âm thủ công phụ thuộc rất nhiều vào mắt nhìn chủ quan và kinh nghiệm của từng người. Bác sĩ A (15 năm kinh nghiệm) nhìn ảnh đoán là Grade 2, nhưng Bác sĩ B (mới ra trường 1 năm) lại chấm là Grade 3 vì thấy túi dịch có vẻ to. Sự lệch pha này gây nguy hiểm cho tính đồng nhất của phác đồ điều trị.
    - **Use Case tiết lộ điều gì:** Khi có AI hỗ trợ trích xuất độ dày vùng ngách trên xương bánh chè (`suprapatellar recess`) và tính tỷ lệ pixel màu Doppler một cách tự động, hệ thống đóng vai trò như một **bộ kiểm tra điều kiện logic khách quan (Deterministic Gatekeeper)**. Nó đưa ra một mức điểm gợi ý dựa trên thuật toán tính toán diện tích chuẩn y khoa, giúp đồng bộ hóa chất lượng chẩn đoán tại bệnh viện. Bác sĩ dù già hay trẻ đều nhìn thấy một cơ sở số liệu minh bạch để đưa ra quyết định cuối cùng.
    - **The Alignment Check:** Qua bóc tách dưới góc nhìn lâm sàng này, bạn đã hiểu vì sao kết quả đầu ra của Use Case này (`Grade 0-3`) lại đóng vai trò là "trái tim mạch máu" cho toàn bộ Dashboard điều trị phía sau chưa, hay bạn muốn chúng ta đào sâu thêm vào điểm nào trước khi thiết kế các tương tác UIX?
- The System suggest what currently being missed from FR and need to define in the UC:
    - **The Gap:** Ambiguous System & Actor Interaction Boundaries inside the Grading Workflow (Thiếu tường minh về ranh giới tương tác giữa Hệ thống và Bác sĩ).
    - **The Question:** How exactly should the doctor **interact** with the system's automated AI calculation when adjusting or validating the suggested severity score (e.g., from Grade 2 to Grade 3)? - The answer of this
        
        The precise, clinically accurate baseline workflow executed by a Diagnostic Radiologist (UP5) consists of the following 6 sequential phases:
        
        - **Step 1 (Patient Posture Standardization):** The clinician places the patient in a supine position with the target knee supported by a bolster in **20°–30° of slight flexion**. This stretches the extensor mechanism (the **Quadriceps/Patellar Tendon)** and eliminates diagnostic tracking errors caused by acoustic anisotropy.
            - Explain with simplification for Software Engineer
                - **The Clinical Action:** The patient lies flat, knee bent exactly 20°–30° over a cushion.
                - **The Software Engineer Analogy:** **Setting up consistent environment variables and running an initialization handshake.**
                - **Deep Jargon Breakdown:**
                    - **Extensor Mechanism - Quadriceps/Patellar Tendon:** Think of this as a mechanical rubber band system (quadriceps muscle → tendon →kneecap → shin bone). When the leg is completely straight, this system sags and wrinkles. Bending it 20°–30° stretches it taut, creating a flat, predictable surface line.
                    - **Acoustic Anisotropy (The Crucial Hardware Bug):** This is a structural physical hardware limitation of ultrasound waves. If the sound beam hits a tendon at a perfect 90° right angle, it bounces back bright white (**Echoic**). If the probe tilts even 5° offline because the tendon is curved/sagging, the wave scatters sideways, and the tissue suddenly registers on-screen as pitch black (**Hypoechoic**), mimicking a fake fluid tear or inflammatory lesion.
                - **Why this matters for your UI/Product Design:** This step is your raw input data sanity check. If the patient isn't positioned right, the ultrasound picture is filled with visual artifact bugs (garbage in, garbage out). Your system needs to know it is processing a standardized 20°–30° landscape view.
        - **Step 2 (Longitudinal Probe Alignment):** The clinician positions a high-frequency linear transducer probe over the midline of the **suprapatellar recess** (sagittal plane), aligning the distal edge over the upper pole of the patella to capture the clear multi-layered layout of the quadriceps tendon.
            - Explain with simplification for SE
                - **The Clinical Action:** The linear probe is placed lengthwise right down the middle of the upper knee, overlapping the top edge of the kneecap.
                - **The Software Engineer Analogy:** **Pointing your API client path to the exact parent database index to unpack a nested multi-layered object arrays.**
                - **Deep Jargon Breakdown:**
                    - **Suprapatellar Recess:** This is the precise target memory location—a pouch-like joint cavity hiding right above the kneecap (**Supra** = above, **Patella** = kneecap) underneath the deep tissue layers.
                    - **Sagittal Plane:** A vertical front-to-back cross-section cut. If your application was a 3D video game engine, this is viewing the joint asset precisely from the orthogonal **Side View Viewport**, rather than looking from the front or top down.
                - **Why this matters for your UI/Product Design:** This gives the system its coordinate system reference frame. In this view, your AI algorithm can run edge detection along standard anatomical landmarks, treating the top edge of the patella as a rock-solid structural zero-point anchor on a 2D canvas.
        - **Step 3 (B-Mode Structural Metric Capture):** Using standard Grey Scale (B-mode), the radiologist identifies the hypoechoic tissue area resting between the *prefemoral fat pad* and the *suprapatellar fat pad*. They visually calculate the maximum vertical distance of joint capsule distension/thickening using the ultrasound console's physical calipers.
            - Explain for SE
                - **The Clinical Action:** The doctor switches to a black-and-white image, identifies the space between two fat patches, and hits two points on the console to calculate the space thickness.
                - **The Software Engineer Analogy:** **Running a 2D Bounding Box Segmentation model to extract a quantitative `float` metric (distance in mm) between two fixed system nodes.**
                - **Deep Jargon Breakdown:**
                    - **B-Mode (Brightness Mode):** This is the baseline structural image format. It transforms reflected sound wave amplitudes into live pixel intensity map arrays (high reflection = white pixels; zero reflection/fluid fluid pools = dark black pixels).
                    - **Hypoechoic Tissue Area:** Any region that absorbs or passes sound waves easily instead of reflecting them, rendering as a dark grey or black signal pool. Inflamed synovial tissue fluid sits in this category.
                    - **Prefemoral & Suprapatellar Fat Pads:** These are your permanent upper and lower hardware guardrail markers. The suprapatellar pouch sits wedged right between them like an expandable buffer queue.
                - **Why this matters for your UI/Product Design:** This is **REQ-RAD-02** in your requirement documentation. The doctor uses manual calipers to measure this space. Your product UI can introduce a digital bounding path box or automated point-to-point drawing tool overlay to automatically extract this distance variable, completely stripping away the manual console math step.
        - **Step 4 (Power Doppler Vascularity Mapping):** The clinician activates the Power Doppler mode on the console, optimizing the wall filter and PRF settings. They carefully hover the probe with **minimal contact pressure** to avoid compressing low-velocity synovial capillaries, visually counting or calculating the percentage area occupied by active blood flow signals inside the suprapatellar landscape.
            - Explain for SE
                - **The Clinical Action:** The doctor switches on the color overlay feature, tweaks the sensitivity filters, and hovers the probe extremely lightly without pressing down into the skin.
                - **The Software Engineer Analogy:** **Activating a live telemetry tracer module with a low-pass noise filter to map active server data traffic volume while avoiding an external physical choke/throttling event.**
                - **Deep Jargon Breakdown:**
                    - **Power Doppler Mode:** A specialized signal tracking sub-routine. Instead of mapping structural tissue borders, it tracks shifts in frequency caused by moving targets (red blood cells). It highlights these regions with bright, glowing color maps overlaid right on top of the black-and-white structural layer.
                    - **Wall Filter & PRF (Pulse Repetition Frequency):** These are variable noise gates. If configured wrong, minor hand tremors will bleed into the visual feed as massive colored pixels (**Clutter Artifact Noise**).
                    - synpvia Capillary Compression Edge Case: If the doctor applies heavy hand force, they manually flatten the tiny micro-blood vessels inside the knee. This physically blocks blood flow, wiping out the signal completely on screen and returning a false negative trace.
                - **Why this matters for your UI/Product Design:** This maps directly to your **Hypervascularity parameter**. Your interface can assist by calculating the ratio of bright color pixels to the total area of the segmented pouch, converting a subjective visual guess into a precise numerical percentage readout.
        - **Step 5 (Semi-Quantitative Grade Synthesis):** The clinician combines both structural metrics mentally against standard musculoskeletal classification tiers: - THE VKIST ML-Module current stop in here
            - *Grade 0 (None):* Completely flat layers; no hypoechoic separation or vascular flow signals.
            - *Grade 1 (Mild):* Thin hypoechoic line running parallel to the femoral bone path; single or minimal isolated vascular blood flow spots.
            - *Grade 2 (Moderate):* Evident hypoechoic expansion pushing the fat pads apart, but lines remain flat; active vascular flow spots occupying less than 50% of the calculated synovial area.
            - *Grade 3 (Severe):* Clear convex or distinct bulging capsule distortion extending outward; intense confluent flow signals covering more than 50% of the calculated synovial landscape.
            - Explain for SE
                - **The Clinical Action:** The doctor looks at both parameters (the pouch thickness + the active color blood flow maps) and maps them to a standard clinical severity tier level (0 to 3).
                - **The Software Engineer Analogy:** **Evaluating raw aggregated metric values against a core business logic conditional switch block (`switch(severityGrade)`) to determine system status codes.**
                - **Deep Tiers Demystified via Code Logic:**
                    - **Grade 0 (Healthy Baseline):**
                        
                        ```jsx
                        if (synovialThickness === 0 && hypervascularityScore === 0) return "Grade 0: Normal Space";
                        ```
                        
                    - **Grade 1 (Mild Inflammation):** Space is filled with a thin, parallel line of tissue expansion; trace color dots show up.JavaScript
                        
                        ```
                        if (synovialThickness > 0 && hypervascularityScore <= 0.10) return "Grade 1: Mild Distension";
                        ```
                        
                    - **Grade 2 (Moderate Inflammation):** The tissue swells enough to visibly push the flanking fat pads apart, and the active blood flow color blocks cover up to half of the pouch container zone.JavaScript
                        
                        ```
                        if (synoviumDistended === true && hypervascularityScore < 0.50) return "Grade 2: Moderate Pouch Deflection";
                        ```
                        
                    - **Grade 3 (Severe Inflammation):** The pouch balloons into a curved, outward bulging geometric form; intense, connected color maps take over more than half of the space landscape.JavaScript
                        
                        ```
                        if (capsuleShape === 'convex_bulge' || hypervascularityScore >= 0.50) return "Grade 3: Critical Structural Flare";
                        ```
                        
        - **Step 6 (Manual Multi-Silo Transcription):** The clinician freezes the optimal reference frames on the hardware console, manually assigns a final severity index label, moves away from the ultrasound machine hardware screen to a desktop workstation PC, and types out the structural text variables into the hospital's Electronic Medical Record (EMR) text block.
            - Explain for SE
                - **The Clinical Action:** The doctor freezes the machine display screen, manually records a final tier index number, stands up, switches chairs to a secondary office computer, logs in, and re-types the exact observations by hand into a text window box.
                - **The Software Engineer Analogy:** **A total lack of system database synchronization. Hand-copying raw log data variables from a separate terminal window and typing them line-by-line into a separate decoupled microservice application.**
                - **Why this matters for your UI/Product Design:** This is the massive core workflow bottleneck. The goal of your upcoming workspace design is to build an interactive, unified web interface bridge. The AI processes the image data parameters natively, renders an automated classification tag proposal directly inside the primary viewing frame, and updates the shared patient record database with 0 manual transcript entries or physical context-switching loops.
    - Additional - from the answer in the `Question` we can model the planUML code solution
        
        !image.png
        
        ```jsx
        @startuml
        ' Settings
        left to right direction
        skin rose
        
        ' Actors
        actor "Diagnostic Radiologist (UP5)" as Rad
        actor "Hospital EMR System" as EMR << System >>
        actor "VKIST AI Pipeline" as AI << System >>
        
        ' System Boundary
        rectangle "VKIST MSK Workspace - Synovitis Grading Engine" {
            
            ' Core Viewing & Extraction Use Cases
            usecase "Load Patient Ultrasound Session" as UC_Load
            usecase "Extract Joint Tissue Metrics" as UC_Extract
            
            ' AI Suggestion Processing
            usecase "Compute Automated Severity Suggestion" as UC_AI_Compute
            usecase "Display Suggestion Tag & Canvas Overlays" as UC_Display
            
            ' Clinician Interaction & Decision Loop
            usecase "Review Suggested Synovitis Grade (0-3)" as UC_Review
            usecase "Manually Override Severity Grade" as UC_Override
            usecase "Sign & Finalize Diagnostic Conclusions" as UC_Finalize
            
            ' Data Sync Hand-off
            usecase "Synchronize Patient Record" as UC_Sync
        }
        
        ' Relationships & Flow Boundaries
        Rad --> UC_Load
        Rad --> UC_Review
        Rad --> UC_Finalize
        
        ' AI Pipeline Interactions
        UC_Load ..> UC_Extract : <<include>>
        UC_Extract --> AI : Transmit raw image streams
        AI --> UC_AI_Compute : Process thickness & Doppler maps
        UC_AI_Compute ..> UC_Display : <<include>>
        
        ' Review and Override Loop
        UC_Display ..> UC_Review : <<include>>
        UC_Override .up.> UC_Review : <<extend>> (If clinician disagrees with AI)
        Rad --> UC_Override
        
        ' Finalization and Sync Hand-offs
        UC_Finalize ..> UC_Sync : <<include>>
        UC_Sync --> EMR : Push standardized JSON structural data
        @enduml
        ```
        
    
    → For the Synovist Grading the interaction between the clinician & system may occur 4 potential case: —> 4 possible interactions
    
    ```jsx
    +-----------------------------------------------------------------------+
    |                       HUMAN-AI CONCURRENT STATES                      |
    +-----------------------------------+-----------------------------------+
    |            QUADRANT 2             |            QUADRANT 1             |
    |   Automation Override Risk        |          True Agreement           |
    |                                   |                                   |
    |   AI: Grade 3 (Accurate)          |   AI: Grade 2 (Accurate)          |
    |   Human: Grade 1 (Oversight)      |   Human: Grade 2 (Confident)      |
    |   Risk: Severe Disease Missed     |   Risk: None (Happy Path)         |
    +-----------------------------------+-----------------------------------+
    |            QUADRANT 4             |            QUADRANT 3             |
    |       Double-Blind Failure        |    Clinician Subservience Risk    |
    |                                   |                                   |
    |   AI: Grade 2 (Boundary Error)    |   AI: Grade 3 (Hallucinated)      |
    |   Human: Grade 1 (Biased Error)   |   Human: Grade 1 (Accurate)       |
    |   Risk: Cascading System Error    |   Risk: Over-treatment Danger     |
    +-----------------------------------+-----------------------------------+
    ```
    
    THE ML-stack use in this scenarios: 
    
    - the grading ML-stack (VKIST-model) → always use (it’s the machine process on the raw-signal from device)
    - the LLM Critic & Actor for acting as explainer on the results of the grading stack (de-blackbox) + conversation with the clinics for pathologic analysis <with RAG> + critic-suggestion  (this LLM shall have to loaded with SKILL / multi-agent system)
    - the LLM-RAG-Referee for prevent bias & blindness of both-side (actor & grader & clinical)
        
        
        | **Referee Role** | **Problem Solved** | **Mechanism** |
        | --- | --- | --- |
        | **1. Unbiased Arbiter** | **Conflict & Bias:** Prevents the LLM from hallucinating to match the clinician's incorrect bias (Confirmation Bias). | Operates as a **Session-State Arbiter**: It ignores conversation history and focuses purely on comparing the raw metrics (`GradCAM maps`, `Doppler indices`) against clinical definitions. |
        | **2. Domain Guardian** | **Knowledge Obsolescence:**Prevents the system from using outdated medical standards (e.g., guidelines from 2020 instead of 2025). | Operates as a **Knowledge-Retrieval Guardian**: It triggers when the system detects high semantic entropy, fetching the *latest* approved academic guidelines to ensure all explanations remain clinically valid. |
    
    The Actor:
    
    - the UP-5 user working with the hardware
    
    4 scenarios can consider