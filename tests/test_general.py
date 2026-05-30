"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Đăng xuất thành công"""
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Click nút "Đăng xuất"
    flutter_click_button(page, "Đăng xuất")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout_success.png"))

    # Assert: Quay về trang đăng nhập (có "Đăng nhập" hoặc ô input Email)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_btn = "Đăng nhập" in sem_text
    has_email_field = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_btn or has_email_field, \
        "TC-11 FAIL: Sau khi đăng xuất không quay về trang đăng nhập"


def test_switch_language_to_english(page, test_config):
    """TC-12: Chuyển ngôn ngữ sang tiếng Anh"""
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Click nút "EN"
    flutter_click_button(page, "EN")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_language_en.png"))

    # Assert: Giao diện hiển thị tiếng Anh
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    english_keywords = ["Logout", "Borrow", "Library", "Search", "Return", "Available"]
    has_english = any(word in sem_text for word in english_keywords)
    assert has_english, \
        f"TC-12 FAIL: Giao diện chưa chuyển sang tiếng Anh. Nội dung: {sem_text[:200]}"
