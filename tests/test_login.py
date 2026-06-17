"""Login tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System.

Covers TC-01..TC-03 plus a librarian-login variant. Assertions are
bilingual-tolerant because the app ships both Vietnamese and English UI text.
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def _wait_for_error(page, *texts, timeout=10000):
    """Smart wait for any of the given error strings (no fixed sleep)."""
    selector = ", ".join(f'flt-semantics:has-text("{t}")' for t in texts)
    page.locator(selector).first.wait_for(state="attached", timeout=timeout)
    enable_flutter_semantics(page)


def _open_login(page, test_config):
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)


def test_login_success(page, test_config):
    """TC-01: Login succeeds with valid credentials."""
    _open_login(page, test_config)
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert test_config["display_name"] in sem_text or "Đăng xuất" in sem_text or "Logout" in sem_text, \
        f"Login failed: display name or logout control not found. Got: {sem_text[:300]}"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fails with a valid email but wrong password."""
    _open_login(page, test_config)
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    _wait_for_error(page, "Mật khẩu không đúng", "Incorrect password")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-02_login_wrong_password.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text or "Incorrect password" in sem_text, \
        f"Expected wrong-password error. Got: {sem_text[:300]}"
    assert "Đăng xuất" not in sem_text, "Should not be logged in after wrong password"


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fails when both fields are empty."""
    _open_login(page, test_config)
    flutter_click_button(page, "Đăng nhập")

    _wait_for_error(page, "Vui lòng nhập email", "Please enter email and password")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-03_login_empty_fields.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng nhập email" in sem_text or "Please enter email and password" in sem_text, \
        f"Expected empty-field validation. Got: {sem_text[:300]}"
    assert "Đăng xuất" not in sem_text, "Should not be logged in when fields are empty"


def test_login_success_librarian(page, test_config):
    """TC-01 (variant): Librarian account shows name/role and the logout control."""
    _open_login(page, test_config)
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-01-librarian_login.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Nguyễn Thủ Thư" in sem_text or "Librarian" in sem_text, \
        f"Expected librarian name/role in AppBar. Got: {sem_text[:300]}"
    assert "Đăng xuất" in sem_text, "Logout button should be visible after login"
