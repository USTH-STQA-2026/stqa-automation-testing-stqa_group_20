# BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG PHẦN MỀM (REPORT.md)
**Dự án**: Hệ thống quản lý mượn sách Thư viện ABC — https://stqa.rbc.vn  
**Phạm vi kiểm thử**: Nhóm 2 — Tìm kiếm & Lọc sách (TC-04 -> TC-07)  
**Nhóm thực hiện**: Nhóm 20  

---

## 1. Phân biệt Software Testing vs Quality Assurance (QA)

Trong kỹ nghệ phần mềm, **Kiểm thử phần mềm (Software Testing)** và **Đảm bảo chất lượng (Quality Assurance - QA)** là hai khái niệm bổ trợ nhưng khác biệt về bản chất:

| Tiêu chí | Kiểm thử phần mềm (Testing) | Đảm bảo chất lượng (QA) |
|---|---|---|
| **Trọng tâm** | Hướng sản phẩm (Product-oriented) | Hướng quy trình (Process-oriented) |
| **Hành động** | Viết automated test, chạy thử nghiệm, chụp ảnh minh chứng, tìm lỗi (Bug-finding). | Đánh giá tính hoàn thiện của quy trình, đề xuất cải tiến quy trình, ngăn ngừa lỗi từ đầu (Bug-prevention). |
| **Mục đích** | Đảm bảo sản phẩm hoạt động đúng yêu cầu thiết kế tại thời điểm hiện tại. | Đảm bảo chất lượng được duy trì ổn định, lâu dài trong suốt vòng đời dự án. |

Báo cáo này đại diện cho phần **QA (Quality Assurance)** nhằm đúc rút kinh nghiệm từ quá trình viết test tự động và đề xuất cải tiến cho toàn bộ hệ thống.

---

## 2. Chi tiết các Test Case đã triển khai (TC-04 -> TC-07)

Dưới đây là mô tả kỹ thuật của 4 kịch bản kiểm thử đã được tự động hóa trong file [test_search.py](file:///D:/Study/Vinh/Study/New%20folder/stqa-automation-testing-stqa_group_20-main/stqa-automation-testing-stqa_group_20-main/tests/test_search.py):

### 🧪 TC-04: Tìm sách theo tên — Tìm thấy kết quả
* **Mục tiêu**: Kiểm tra tính năng tìm kiếm trả về đúng sách khi tìm bằng từ khóa khớp với tên sách.
* **Các bước tự động**:
  1. Đăng nhập qua tài khoản thành viên mặc định (`login`).
  2. Nhập từ khóa `"Flutter"` vào ô tìm kiếm bằng `flutter_fill`.
  3. Đợi 2 giây để giao diện Flutter cập nhật và kích hoạt lại semantics tree.
  4. Chụp ảnh màn hình làm bằng chứng (`TC-04_search_book_by_name.png`).
* **Test Oracle**: Kiểm tra số lượng phần tử `flt-semantics` có thuộc tính `aria-label` chứa từ khóa `"Flutter"` phải lớn hơn 0 (`count() > 0`).

### 🧪 TC-05: Tìm sách — Không có kết quả
* **Mục tiêu**: Kiểm tra hệ thống xử lý chính xác khi người dùng tìm kiếm bằng từ khóa không khớp với bất kỳ đầu sách nào.
* **Các bước tự động**:
  1. Đăng nhập qua tài khoản thành viên mặc định.
  2. Nhập từ khóa không tồn tại `"xyz_khong_ton_tai_12345"` vào ô tìm kiếm.
  3. Đợi 2 giây và kích hoạt lại semantics tree.
  4. Chụp ảnh màn hình làm bằng chứng (`TC-05_search_book_no_result.png`).
* **Test Oracle (Strong)**:
  - Kiểm tra số lượng card sách hiển thị (`aria-label*="Mã: BOOK"`) phải bằng 0.
  - Kiểm tra xem thông báo lỗi hiển thị trên giao diện có chứa cụm từ `"Không tìm thấy sách"` hoặc `"No books found"` hay không.

### 🧪 TC-06: Lọc sách theo thể loại "Công nghệ"
* **Mục tiêu**: Kiểm tra bộ lọc thể loại hoạt động chính xác, chỉ hiển thị sách thuộc đúng thể loại đã lọc.
* **Các bước tự động**:
  1. Đăng nhập qua tài khoản thành viên mặc định.
  2. Nhập `"Công nghệ"` vào ô lọc thể loại.
  3. Đợi 2 giây và kích hoạt lại semantics tree.
  4. Chụp ảnh màn hình làm bằng chứng (`TC-06_filter_by_category.png`).
* **Test Oracle (Strong - Toàn diện)**:
  - Kiểm tra danh sách sách trả về có lớn hơn 0.
  - Duyệt qua từng card sách hiển thị (`aria-label*="Mã: BOOK"`) và đảm bảo rằng thuộc tính `aria-label` của mỗi card đều chứa từ khóa `"Công nghệ"` (hoặc `"Technology"`).

### 🧪 TC-07: Tìm sách theo tác giả
* **Mục tiêu**: Kiểm tra tính năng tìm kiếm theo tên tác giả trả về các sách tương ứng do tác giả đó viết.
* **Các bước tự động**:
  1. Đăng nhập qua tài khoản thành viên mặc định.
  2. Nhập tên tác giả `"Nguyễn Minh Đức"` vào ô tìm kiếm.
  3. Đợi 2 giây và kích hoạt lại semantics tree.
  4. Chụp ảnh màn hình làm bằng chứng (`TC-07_search_by_author.png`).
* **Test Oracle**: Kiểm tra số lượng phần tử `flt-semantics` có thuộc tính `aria-label` chứa tên tác giả `"Nguyễn Minh Đức"` phải lớn hơn 0.

---

## 3. Đánh giá chất lượng tính năng "Tìm kiếm & Lọc"

Qua quá trình thực thi kiểm thử tự động, chúng tôi đưa ra các nhận xét chất lượng như sau:

* **Tính chính xác (Accuracy)**: Hệ thống thực hiện tìm kiếm và lọc dữ liệu chính xác theo dữ liệu mẫu (Seed Data) định sẵn.
* **Độ nhạy chữ hoa/thường (Case Insensitivity)**: Tính năng tìm kiếm đáp ứng tốt tiêu chuẩn không phân biệt chữ hoa hay chữ thường (ví dụ: tìm `"flutter"` vẫn ra sách `"Lập trình Flutter cơ bản"`).
* **Trải nghiệm người dùng (UX) khi không có kết quả**: Hệ thống có thông báo rõ ràng `"Không tìm thấy sách"` thay vì chỉ để màn hình trống, giúp người dùng định vị được trạng thái hệ thống.

---

## 4. Đánh giá quy trình Kiểm thử tự động (Process Evaluation)

### 4.1. Ứng dụng Mô hình RIPR (Chương 2 - Textbook)
Mỗi test case tự động được thiết kế chặt chẽ theo mô hình RIPR để đảm bảo tối ưu hóa khả năng phát hiện lỗi:
1. **Reachability (Khả năng chạm tới)**: Điều hướng thành công đến trang chủ sau khi qua bước `login`.
2. **Infection (Sự nhiễm lỗi)**: Nhập các chuỗi tìm kiếm biên hoặc không hợp lệ (nhập chuỗi rác) để đưa hệ thống vào các trạng thái dữ liệu khác nhau.
3. **Propagation (Sự lan truyền)**: Đợi 2 giây (`wait_for_timeout`) để dữ liệu tìm kiếm cập nhật từ bộ nhớ và lan truyền ra giao diện người dùng.
4. **Revealability (Khả năng bộc lộ lỗi)**: Sử dụng các Assertion mạnh (như duyệt vòng lặp qua từng phần tử lọc ở TC-06) thay vì kiểm tra hời hợt, giúp bộc lộ lỗi ngay lập tức nếu bộ lọc hoạt động sai lệch.

### 4.2. Giải quyết đặc thù Flutter Web CanvasKit
Khác với các ứng dụng Web HTML truyền thống, Flutter Web render giao diện trên thẻ `<canvas>`.
* **Thách thức**: Không thể dùng các CSS Selector tiêu chuẩn để định vị phần tử.
* **Giải pháp**: 
  - Kích hoạt Accessibility Semantics Tree thông qua hàm `enable_flutter_semantics(page)`.
  - Tương tác với các trường nhập liệu thông qua `aria-label` đại diện.
  - Sử dụng chiến lược Smart Wait (chờ semantics sẵn sàng) để giảm thiểu tối đa hiện tượng **Flaky Tests** (test chạy lúc pass lúc fail do độ trễ kết xuất giao diện).

---

## 5. Đề xuất cải tiến hệ thống & quy trình (QA Recommendations)

Để nâng cao chất lượng phần mềm và tính ổn định lâu dài, chúng tôi đề xuất các cải tiến sau:

1. **Cải tiến phía Hệ thống (Application under test)**:
   - **Debounce Search**: Hiện tại tìm kiếm đang cập nhật rất nhanh trên mỗi ký tự nhập vào. Cần thêm cơ chế debounce (trễ ~300ms sau khi ngừng gõ) để tối ưu hiệu năng render canvas.
   - **Tối ưu hóa Semantics Tree**: Cần gắn nhãn `aria-label` chi tiết hơn cho từng nút bấm hoặc khối văn bản để hỗ trợ tốt hơn cho cả người dùng khiếm thị và các công cụ kiểm thử tự động.

2. **Cải tiến quy trình Kiểm thử (Testing Process)**:
   - **Tích hợp CI/CD**: Thiết lập luồng GitHub Actions tự động chạy toàn bộ suite test mỗi khi có Pull Request mới.
   - **Regression Test Selection**: Khi hệ thống cập nhật cấu trúc dữ liệu hoặc danh sách sách, chỉ cần chạy lại nhóm test Tìm kiếm/Lọc và Mượn/Trả, giúp tiết kiệm thời gian chạy kiểm thử trên server CI.

---

## 6. Khai báo sử dụng AI

Nhóm thực hiện đã phối hợp sử dụng trợ lý AI **Antigravity** phát triển bởi Google DeepMind để:
- Hỗ trợ phân tích tài liệu đặc tả yêu cầu phần mềm (SRS).
- Sinh mã khung và các đoạn kiểm tra kết quả (Test Oracles) trong file `tests/test_search.py` dựa trên semantics tree.
- Hỗ trợ định dạng báo cáo đánh giá chất lượng phần mềm.

Đội ngũ đã thực hiện đối chiếu, soát lỗi kỹ lưỡng toàn bộ mã nguồn do AI sinh ra đối với tài liệu SRS để đảm bảo tính chính xác và loại bỏ các lỗi flaky liên quan đến thời gian chờ kết xuất.
