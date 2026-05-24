"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password (*Đăng nhập thất bại – sai mật khẩu*)

    Manual TC-04: Email đúng (librarian@library.com) nhưng sai mật khẩu →
    Hệ thống ở lại trang đăng nhập và hiển thị "Incorrect password."

    📖 RIPR:
        [R] Truy cập trang đăng nhập
        [I] Nhập email đúng nhưng mật khẩu sai → kích hoạt trạng thái lỗi
        [P] Lỗi lan truyền ra thông báo trên UI
        [R✓] Kiểm tra thông báo lỗi, không có nút Đăng xuất
    """
    # [R] Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Enter valid email with wrong password
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    # [P] Wait for Flutter to process; re-enable semantics to capture error state
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-02_login_wrong_password.png"))

    # [R✓] Error message shown, user not logged in
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Incorrect password" in sem_text or "Mật khẩu không đúng" in sem_text, \
        f"Expected wrong-password error message. Got: {sem_text[:300]}"
    assert "Đăng xuất" not in sem_text, \
        "Should not be logged in after wrong password"


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail – empty fields (*Đăng nhập thất bại – để trống các trường*)

    Manual TC-05: Bấm Đăng nhập khi cả hai trường trống →
    Hệ thống hiển thị "Please enter email and password."

    📖 RIPR:
        [R] Truy cập trang đăng nhập
        [I] Không nhập gì, bấm Đăng nhập → kích hoạt validation
        [P] Validation lỗi lan truyền ra thông báo
        [R✓] Kiểm tra thông báo validation, không có nút Đăng xuất
    """
    # [R] Navigate to login page (fields are empty by default)
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Click login immediately without entering credentials
    flutter_click_button(page, "Đăng nhập")

    # [P] Wait for Flutter to process; re-enable semantics to capture validation state
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-03_login_empty_fields.png"))

    # [R✓] Validation message shown, user not logged in
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Please enter email and password" in sem_text or "Vui lòng nhập email" in sem_text, \
        f"Expected empty-field validation message. Got: {sem_text[:300]}"
    assert "Đăng xuất" not in sem_text, \
        "Should not be logged in when fields are empty"


def test_login_success_librarian(page, test_config):
    """TC-01: — Librarian login (*Đăng nhập thành công bằng tài khoản Librarian*)

    Manual TC-01: librarian@library.com / admin123 →
    AppBar hiển thị tên + "(Librarian)", thấy đủ 3 tab: Sách, Mượn/Trả, Thành viên.

    📖 RIPR: Giống TC-01 nhưng dùng tài khoản Librarian cố định.
    """
    # [R] Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Enter Librarian credentials
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Wait for main page to load
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-01-librarian_login.png"))

    # [R✓] Librarian name + role displayed, Logout button visible
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Nguyễn Thủ Thư" in sem_text or "Librarian" in sem_text, \
        f"Expected librarian name/role in AppBar. Got: {sem_text[:300]}"
    assert "Đăng xuất" in sem_text, "Logout button should be visible after login"
