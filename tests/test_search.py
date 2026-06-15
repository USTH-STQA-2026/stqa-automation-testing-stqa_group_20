"""Search & filter tests (*Kiểm thử Tìm kiếm & Lọc sách*) — TC-04..TC-07.

Selectors used:
    - Search box aria-label:    "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Book card: flt-semantics[role="group"][aria-label*="Mã: BOOK"]
"""
import os
from conftest import enable_flutter_semantics, flutter_fill, login, SCREENSHOT_DIR

SEARCH_BOX = "Tìm kiếm theo tên sách hoặc tác giả..."
CATEGORY_FILTER = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
BOOK_CARD = 'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'


def test_search_book_by_name(page, test_config):
    """TC-04: Searching "Flutter" returns at least one matching book."""
    login(page, test_config)
    flutter_fill(page, SEARCH_BOX, "Flutter")

    page.locator(BOOK_CARD).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-04_search_book_by_name.png"))

    assert page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0, \
        "No books containing 'Flutter' found in search results"


def test_search_book_no_result(page, test_config):
    """TC-05: A non-existent keyword shows no book cards and a 'not found' message."""
    login(page, test_config)
    flutter_fill(page, SEARCH_BOX, "xyz_khong_ton_tai_12345")

    # Wait for the empty-state message rather than a fixed sleep.
    page.locator(
        'flt-semantics:has-text("Không tìm thấy sách"), flt-semantics:has-text("No books found")'
    ).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-05_search_book_no_result.png"))

    assert page.locator(BOOK_CARD).count() == 0, "Expected no book cards for a non-existent keyword"
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Không tìm thấy sách" in sem_text or "No books found" in sem_text, \
        f"Expected a 'no results' message. Got: {sem_text[:300]}"


def test_filter_by_category(page, test_config):
    """TC-06: Filtering by 'Công nghệ' returns only Technology books."""
    login(page, test_config)
    flutter_fill(page, CATEGORY_FILTER, "Công nghệ")

    page.locator(BOOK_CARD).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-06_filter_by_category.png"))

    books = page.locator(BOOK_CARD)
    count = books.count()
    assert count > 0, "No books found under 'Công nghệ' category filter"
    for i in range(count):
        label = books.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label or "Technology" in label, \
            f"Book card does not belong to 'Công nghệ': {label}"


def test_search_by_author(page, test_config):
    """TC-07: Searching an author name returns at least one matching book."""
    login(page, test_config)
    flutter_fill(page, SEARCH_BOX, "Nguyễn Minh Đức")

    page.locator(BOOK_CARD).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-07_search_by_author.png"))

    assert page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0, \
        "No books by 'Nguyễn Minh Đức' found in search results"
