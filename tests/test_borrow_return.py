"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Lưu ý tài khoản:
  - TC-08 dùng dam.tran@email.com (chưa mượn sách — phù hợp test mượn)
  - TC-09, TC-10 dùng ba.nguyen@email.com (đang mượn BOOK003)
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)
    """
    # Arrange: Đăng nhập bằng tài khoản chưa mượn sách (dam.tran@email.com)
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "dam.tran@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Act: Tìm sách có trạng thái "Có sẵn"
    book_card = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    book_card.wait_for(state="attached", timeout=10000)
    
    # Click nút "Mượn sách này" trong card sách đó
    borrow_btn = book_card.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()
    
    # Đợi dialog xác nhận và bật lại semantics
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Click nút "Mượn" (xác nhận trong dialog)
    confirm_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn")')
    confirm_btn.wait_for(state="attached", timeout=5000)
    confirm_btn.click()
    
    # Chờ xử lý hoàn thành
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Chụp screenshot kết quả
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # Assert: "Đang mượn" hoặc "thành công" xuất hiện trong semantics
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đang mượn" in sem_text or "thành công" in sem_text, \
        "TC-08 FAIL: Không thấy trạng thái 'Đang mượn' hoặc thông báo thành công"


def test_view_borrowed_books(page, test_config):
    """TC-09: Xem danh sách sách đang mượn trong tab 'Mượn / Trả'"""
    # Arrange: Đăng nhập bằng tài khoản đang mượn sách (ba.nguyen có BOOK003)
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Act: Click vào tab "Mượn / Trả"
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    # Assert: Có sách đang mượn hoặc có nút "Trả sách"
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrowed = "Đang mượn" in sem_text
    has_return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').count() > 0
    assert has_borrowed or has_return_btn, \
        "TC-09 FAIL: Không thấy sách đang mượn trong tab Mượn / Trả"


def test_return_book(page, test_config):
    """TC-10: Trả sách đang mượn"""
    # Arrange: Đăng nhập bằng tài khoản đang mượn sách
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Act: Click tab "Mượn / Trả" → tìm nút "Trả sách"
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.wait_for(state="attached", timeout=10000)
    return_btn.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    # Assert: Thông báo thành công hoặc sách chuyển về "Có sẵn"
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Có sẵn" in sem_text or "Trả sách" not in sem_text, \
        "TC-10 FAIL: Trả sách không thành công"
