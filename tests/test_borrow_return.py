"""Borrow & return tests (*Kiểm thử Mượn & Trả sách*) — TC-08..TC-10.

Accounts:
    - TC-08 uses dam.tran@email.com (no active borrows — a clean slate for borrowing).
    - TC-09/TC-10 use test_config (ba.nguyen@email.com, MEM002, currently borrowing BOOK003).
"""
import os
from playwright.sync_api import expect
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)

BORROW_TAB = 'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'


def _login_as(page, base_url, email, password):
    page.goto(base_url, wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)


def _open_borrow_tab(page):
    page.locator(BORROW_TAB).first.click()
    enable_flutter_semantics(page)


def test_borrow_book(page, test_config):
    """TC-08: Borrowing an available book succeeds and creates a borrow record."""
    _login_as(page, test_config["base_url"], "dam.tran@email.com", "password123")

    # Borrow the first available book via the button inside its card.
    book_card = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    book_card.wait_for(state="attached", timeout=10000)
    book_card.get_by_role("button", name="Mượn sách này").first.click()

    # Confirm in the dialog. exact=True avoids matching "Mượn sách này" / the "Mượn / Trả" tab.
    wait_for_flutter(page, text="Xác nhận")
    page.get_by_role("button", name="Mượn", exact=True).click()

    # Primary oracle: explicit success toast.
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # Status lives in the group's aria-label (seed records) or its text (fresh records).
    _open_borrow_tab(page)
    record = page.locator(
        'flt-semantics[role="group"][aria-label*="Đang mượn"], '
        'flt-semantics[role="group"]:has-text("Đang mượn")'
    ).first
    expect(record, "TC-08: no 'Đang mượn' borrow record after borrowing").to_be_visible()


def test_view_borrowed_books(page, test_config):
    """TC-09: The Mượn / Trả tab lists the member's borrowed book."""
    login(page, test_config)
    _open_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    record = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]').first
    expect(record, "TC-09: no borrowed book shown in Mượn / Trả tab").to_be_visible()


def test_return_book(page, test_config):
    """TC-10: Returning a borrowed book updates its record to 'Đã trả'."""
    login(page, test_config)
    _open_borrow_tab(page)

    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.wait_for(state="attached", timeout=10000)
    return_btn.click()

    wait_for_flutter(page, text="thành công")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    returned = page.locator('flt-semantics').filter(has_text="Đã trả").first
    expect(returned, "TC-10: returned record does not show 'Đã trả'").to_be_visible()
