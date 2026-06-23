# VKIST ULTRASOUND - TÀI LIỆU HƯỚNG DẪN & GIỚI THIỆU DỰ ÁN

---

## 1. Giới thiệu chung

VKIST Ultrasound là hệ thống hỗ trợ chẩn đoán viêm khớp gối tiên tiến ứng dụng Trí tuệ nhân tạo (AI). Hệ thống giúp bác sĩ phân tích hình ảnh siêu âm một cách tự động, từ việc nhận diện chính xác góc chụp đến việc đo đạc các chỉ số bệnh lý phức tạp. Qua đó, giải pháp này giúp tối ưu hóa quy trình khám chữa bệnh, giảm thiểu sai sót chủ quan và nâng cao hiệu suất làm việc tại các cơ sở y tế.

---

## 2. Quy trình xử lý toàn diện (AI Pipeline Workflow)

Hệ thống vận hành theo một quy trình khép kín, tự động phân nhánh logic dựa trên tính chất hình ảnh đầu vào:

1. **Tiếp nhận & Tiền xử lý ảnh:** Tải ảnh siêu âm thô lên hệ thống. AI tự động áp dụng thuật toán tăng cường tương phản CLAHE để làm rõ nét các cấu trúc giải phẫu bị mờ hoặc nhiễu.


2. **Phân loại góc chụp (Angle Classification):** Tự động xác định tư thế chụp/mặt cắt nhằm kích hoạt nhánh pipeline phân tích chuyên biệt.


3. **Phát hiện Viêm (Inflammation Detection):** Đánh giá sơ bộ sự hiện diện của dịch khớp hoặc tình trạng tăng sinh màng hoạt dịch.


4. **Phân vùng & Đo đạc (Segmentation & Measurement):** Tách biệt các lớp mô giải phẫu (xương, dịch, màng, gân...) và tự động xác định độ dày tổn thương tại các vùng trọng yếu.


5. **Đánh giá mức độ nặng (Severity Scoring):** Tính toán chỉ số tổng hợp để phân cấp mức độ viêm khớp.


6. **Quản lý hồ sơ & Báo cáo:** Lưu trữ dữ liệu chuẩn hóa vào hệ thống nội bộ và kết xuất phiếu kết quả khám bệnh dạng PDF.



Dưới đây là sơ đồ luồng logic của hệ thống được thiết kế bằng **PlantUML** giúp lập trình viên backend dễ dàng triển khai:

```plantuml
@startuml
skinparam handwritten false
skinparam monochrome false
skinparam packageStyle rect
skinparam shadowing true

title SƠ ĐỒ ĐIỀU HƯỚNG LOGIC PIPELINE - VKIST ULTRASOUND AI

start

:Tiếp nhận ảnh siêu âm từ Web UI;
:Áp dụng thuật toán tiền xử lý CLAHE (Tăng cường độ nét);

:Mô hình Phân loại góc chụp (Angle Model);
note right: Tích hợp ConvNeXt / Swin / DenseNet

if (Góc chụp hợp lệ?) then (Không thuộc góc Sup_up_long / Post_trans)
    :Hiển thị nhãn góc chụp (ví dụ: Med-Lat Long);
    :Thông báo lỗi: Góc chụp đầu vào không hỗ trợ xử lý tiếp;
    stop
else (Hợp lệ)
    :Mô hình Phát hiện viêm (EfficientNet-B0);
    
    if (Trạng thái ổ khớp?) then (Không viêm)
        :Hiển thị trạng thái KHÔNG VIÊM trên giao diện;
        :Cho phép nhập thông tin và lưu trữ cơ bản;
    else (Có viêm)
        :Hiển thị trạng thái CÓ VIÊM;
        
        if (Góc chụp phát hiện?) then (Post_trans)
            :Chạy phân đoạn vùng tổn thương (DeepLabV3-ResNet101);
            :Khoanh vùng, gắn nhãn màu Nang Baker (Baker's Cyst);
        else (Sup_up_long / Suprapat)
            :Chạy phân đoạn vùng tổn thương (DeepLabV3-ResNet50);
            partition "Thuật toán Đo đạc thông minh" {
                :Smart ROI (Tập trung 1/3 khu vực giữa);
                :Continuous Segment Search (Tìm đoạn dịch liên tục dài nhất);
                :Xác định độ dày ổ dịch/màng hoạt dịch (mm);
            }
            :Tính điểm toán học phân cấp Mức độ bệnh (Cấp 0 -> 3);
        endif
    fi
endif

split
    :Nhập thông tin bệnh nhân & Chẩn đoán lâm sàng;
    :Lưu trữ cấu trúc thư mục nội bộ (patients/);
split again
    :Xuất phiếu kết quả khám bệnh dạng PDF (report.pdf);
end split

stop
@enduml

```

---

## 3. Các Tính năng Chi tiết & Mô hình học máy

### 3.1. Hệ thống Mô hình AI Đa dạng (Multi-Model Architecture)

* **Khối Phân loại Góc chụp:** Tích hợp các kiến trúc mạng mạng nơ-ron tiên tiến (SOTA) bao gồm ConvNeXt-Tiny (đạt độ chính xác tuyệt đối 100% trên tập kiểm thử) , Swin Transformer, và DenseNet. Hệ thống mặc định sử dụng ConvNeXt làm lõi phân loại chính đầu tiên cho mọi ảnh.


* **Khối Phân vùng (Semantic Segmentation):** Hỗ trợ linh hoạt các mô hình DeepLabV3+ (hoặc DeepLabV3-ResNet50 với độ chính xác 91.67%), UNet3+ Attention, và EfficientFeedback. Các cấu trúc này được tối ưu hóa sâu nhằm nhận diện chính xác đường biên ranh giới màng hoạt dịch phức tạp.



### 3.2. Tính năng Đo đạc Thông minh (Smart Measurement)

Nhánh xử lý góc `Sup_up_long` tích hợp hai thuật toán hình học độc quyền nhằm loại bỏ sai số đo đạc:

* **Smart ROI:** Hệ thống tự động khoanh vùng và tập trung phân tích vào khu vực 1/3 chính giữa của vùng nghi ngờ, nơi có giá trị và chỉ số chẩn đoán lâm sàng cao nhất.


* **Continuous Segment Search:** Thuật toán tự động tìm kiếm đoạn mặt nạ (mask) liên tục dài nhất. Cơ chế này đảm bảo kết quả tính toán độ dày của màng và dịch khớp phản ánh đúng thực tế, khách quan và không bị ảnh hưởng bởi nhiễu ảnh cục bộ.



### 3.3. Phân cấp Mức độ Bệnh (Severity Classification)

Hệ thống tính toán chỉ số kết hợp giữa diện tích dịch khớp tụ và mức độ tăng sinh màng hoạt dịch để phân định thành 4 cấp độ bệnh lý rõ ràng:

| Cấp độ viêm | Phân loại lâm sàng | Đặc điểm cấu trúc hình ảnh siêu âm |
| --- | --- | --- |
| **Cấp 0** | Rất nhẹ | Lượng dịch khớp nằm trong giới hạn sinh lý bình thường.|
| **Cấp 1** | Nhẹ | Lớp dịch khớp mỏng, xuất hiện tăng sinh màng hoạt dịch mức độ nhẹ.|
| **Cấp 2** | Trung bình | Lượng dịch khớp và màng hoạt dịch tăng sinh phì đại rõ rệt.|
| **Cấp 3** | Nặng | Ổ dịch khớp dày, màng hoạt dịch phát triển mạnh và xâm lấn sâu.|

---

## 4. Đặc tả Giao diện & Hướng dẫn Vận hành Hệ thống

Giao diện Web UI của ứng dụng được thiết kế phân cấp tối giản theo bố cục 3 luồng dọc: **Bảng trái (Cấu hình Mô hình)** $\rightarrow$ **Bảng giữa (Tải ảnh & Hiển thị)** $\rightarrow$ **Bảng phải (Nhập dữ liệu & Xem kết quả phân tích)**.

### Quy trình vận hành 4 bước dành cho Bác sĩ:

#### Bước 1: Cấu hình Mô hình AI (Left Panel)

* Trước khi tiến hành tải ảnh siêu âm, bác sĩ có thể linh hoạt tùy chọn thuật toán AI mong muốn cho từng block tác vụ tại bảng điều khiển bên trái. Hệ thống đã được cấu hình mặc định sẵn các mô hình tối ưu nhất.



#### Bước 2: Tải ảnh siêu âm lên hệ thống (Middle Panel)

* Bác sĩ thực hiện kéo thả tập tin ảnh trực tiếp vào vùng nhận diện hoặc nhấn nút `"Chọn ảnh"`.


* Ngay sau khi tệp tin được nạp, hệ thống sẽ tự động kích hoạt toàn bộ Pipeline phân tích ngầm theo luồng xử lý tự động.



#### Bước 3: Đọc kết quả phân tích tự động từ AI (Right Panel & Modal Popup)

Hệ thống tự động hiển thị kết quả trực quan dựa trên nhãn mặt cắt nhận diện được:

* 
**Trường hợp góc chụp không hỗ trợ (ví dụ: `Med-Lat Long`):** Hệ thống lập tức xuất nhãn cảnh báo màu tím `"GÓC CHỤP: Med-Lat Long"` và dừng tiến trình xử lý tiếp theo.


* 
**Trường hợp góc mặt sau `Post_trans`:** Hệ thống kiểm tra tình trạng viêm. Nếu có viêm, ảnh phân đoạn sẽ hiển thị màu overlay trực quan khoanh vùng chính xác ổ tổn thương **Nang Baker** (Baker's cyst) kèm bảng chú thích màu sắc mô giải phẫu tương ứng.


* 
**Trường hợp góc mặt trước `Sup_up_long`:** Hệ thống tiến hành phân đoạn, hiển thị đường lưới đo đạc thông minh. Đồng thời tính toán chi tiết độ dày ổ dịch bằng đơn vị milimét ($mm$) và đưa ra chẩn đoán mức độ viêm chính xác.



#### Bước 4: Lưu trữ hồ sơ dữ liệu & Xuất bản phiếu khám lâm sàng

* Bác sĩ thực hiện điền đầy đủ thông tin vào form biểu mẫu bệnh nhân ở bảng bên phải (Trong đó hai trường dữ liệu **Mã bệnh nhân** và **Họ và tên** là bắt buộc). Ghi nhận thêm nhận xét lâm sàng cá nhân vào ô "Chẩn đoán của bác sĩ".


* Nhấn nút `"Lưu dữ liệu"` để hệ thống đóng gói và lưu trữ nội bộ vào máy chủ.


* Nhấn nút `"Xuất phiếu khám (PDF)"` để tải về máy mẫu phiếu in kết quả y khoa chính thức trả cho bệnh nhân.



---

## 5. Đặc tả Kiến trúc Lưu trữ Dữ liệu Đầu ra

### 5.1. Cấu trúc cây thư mục lưu trữ hồ sơ bệnh nhân (Storage Structure)

Khi bác sĩ nhấn chọn chức năng lưu trữ dữ liệu , hệ thống tự động khởi tạo cấu trúc thư mục phân cấp động theo mốc thời gian thực tại phân vùng `patients/` nhằm tránh trùng lặp thông tin:

```text
patients/
└── <Mã_Bệnh_Nhân>_<Họ_Và_Tên_Không_Dấu>/
    └── <NamThangNgay>_<GioPhutGiay>/
        ├── info.txt         # Tệp tin cấu trúc lưu trữ siêu dữ liệu định lượng của ca bệnh
        ├── original.png     # File hình ảnh siêu âm gốc (hoặc ảnh đã tăng cường CLAHE)
        ├── segmented.png    # File ảnh overlay mặt nạ phân đoạn màu từ AI mô hình
        └── report.pdf       # File phiếu kết quả chẩn đoán y khoa chính thức xuất cho bệnh nhân

```

*Ví dụ thực tế:* `patients\BN0001_Nguyen_Van_A\20260505_170011\` 

### 5.2. Định dạng cấu trúc tệp dữ liệu `info.txt`

Tệp tin `info.txt` đóng vai trò lưu trữ toàn bộ thông tin tối giản, giúp hệ thống hoặc các agent xử lý số liệu có thể dễ dàng phân tích (parse) dữ liệu mà không cần đọc file PDF:

```text
--- THÔNG TIN BỆNH NHÂN ---
Mã bệnh nhân: BN0001
Họ tên: Nguyễn Văn A
Giới tính: Nam
Tuổi: 88
Ghi chú lâm sàng: Tràn dịch và có thể viêm

--- KẾT QUẢ PHÂN TÍCH AI ---
Góc chụp: sup-up-long (99.93%)
Viêm nhiễm: Có (94.44%)
Độ dày màng: 6.53 mm (95 px)
Vị trí x: 420
Mức độ: Trung bình
Mô tả: Dịch khớp trung bình (51px), màng hoạt dịch tăng sinh vừa

```

(Ghi chú: Nội dung trên được ánh xạ chính xác từ các chỉ số định lượng thu được qua mô hình phân đoạn hình học của hệ thống ).

### 5.3. Quy chuẩn nội dung phiếu kết quả y khoa `report.pdf`

Phiếu kết quả chẩn đoán hình ảnh dạng PDF được tạo tự động với cấu trúc bố cục chuẩn hóa y tế gồm 4 phần chính:

1. 
**Thông tin Cơ sở & Tiêu đề:** Biểu trưng nhận diện VKIST, tên "TRUNG TÂM CHẨN ĐOÁN HÌNH ẢNH VKIST", địa chỉ "Khu Công nghệ cao Hòa Lạc, Thạch Thất, Hà Nội" kèm tiêu đề lớn **"PHIẾU KẾT QUẢ SIÊU ÂM KHỚP GỐI"**.


2. I. Thông tin bệnh nhân: Hiển thị chi tiết Họ tên, Giới tính, Mã BN, Tuổi của người bệnh.


3. II. Hình ảnh siêu âm: Chèn song song hai khung hình trực quan bao gồm `Hình 1: Ảnh gốc / Tăng cường` và `Hình 2: Ảnh phân đoạn AI` (có kèm sơ đồ lưới đo đạc và chú thích màu).


4. **III. Kết quả phân tích tự động (AI Metric):**
* Góc chụp dự đoán đạt tỷ lệ tương ứng (Ví dụ: `sup-up-long` - Độ tin cậy: `99.93%`).


* Tình trạng viêm ổ khớp (Ví dụ: `Có khả năng viêm` - Độ tin cậy: `94.44%`).


* Chỉ số đo đạc vật lý: Độ dày dịch & màng hoạt dịch tính toán được đạt mức `6.53 mm`.


* Đánh giá mức độ viêm tổng hợp: `Trung bình`.


* Chi tiết mô tả định lượng: Dịch khớp trung bình ($51\text{ px}$), màng hoạt dịch tăng sinh vừa ($95\text{ px}$).



5. IV. Chẩn đoán và kết luận của Bác sĩ: Trích xuất nguyên vẹn nội dung ghi chú lâm sàng do bác sĩ trực tiếp nhập vào hệ thống (Ví dụ: `"Tràn dịch và có thể viêm"`).