"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
    """
    login(page, test_config)
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    
    # Wait for Flutter semantics tree to update
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Take screenshot for reporting
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-04_search_book_by_name.png"))
    
    # Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    flutter_books_count = page.locator('flt-semantics[aria-label*="Flutter"]').count()
    assert flutter_books_count > 0, "No books containing 'Flutter' found in search results"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
    """
    login(page, test_config)
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")
    
    # Wait for Flutter semantics tree to update
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Take screenshot for reporting
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-05_search_book_no_result.png"))
    
    # Verify: no book cards exist
    book_cards_count = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count()
    assert book_cards_count == 0, f"Expected 0 books, but found {book_cards_count}"
    
    # Retrieve all semantics text contents to check for "no results" message
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Không tìm thấy sách" in sem_text or "No books found" in sem_text, \
        f"Expected 'Không tìm thấy sách' or 'No books found' in semantics tree, but got: {sem_text[:300]}"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
    """
    login(page, test_config)
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
    
    # Wait for Flutter semantics tree to update
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Take screenshot for reporting
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-06_filter_by_category.png"))
    
    # Get all book cards
    books_locator = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    books_count = books_locator.count()
    assert books_count > 0, "No books found under 'Công nghệ' category filter"
    
    # Verify each book belongs to 'Công nghệ'
    for i in range(books_count):
        label = books_locator.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in label or "Technology" in label, \
            f"Book card '{label}' does not belong to 'Công nghệ' category"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
    """
    login(page, test_config)
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
    
    # Wait for Flutter semantics tree to update
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Take screenshot for reporting
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-07_search_by_author.png"))
    
    # Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    author_books_count = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count()
    assert author_books_count > 0, "No books by 'Nguyễn Minh Đức' found in search results"

