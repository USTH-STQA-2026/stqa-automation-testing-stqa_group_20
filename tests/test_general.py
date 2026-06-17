"""Logout & language tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — TC-11, TC-12."""
import os
from conftest import enable_flutter_semantics, flutter_click_button, wait_for_flutter, login, SCREENSHOT_DIR


def test_logout(page, test_config):
    """TC-11: Logging out returns to the login screen."""
    login(page, test_config)
    flutter_click_button(page, "Đăng xuất")

    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout_success.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_email_field = page.locator('input[aria-label="Email"]').count() > 0
    assert "Đăng nhập" in sem_text or has_email_field, \
        "TC-11: login screen not shown after logout"


def test_switch_language_to_english(page, test_config):
    """TC-12: Clicking 'EN' switches the UI to English."""
    login(page, test_config)
    flutter_click_button(page, "EN")

    # Wait for any English label to appear instead of a fixed sleep.
    page.locator(
        ", ".join(f'flt-semantics:has-text("{w}")' for w in ("Logout", "Borrow", "Library", "Search"))
    ).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_language_en.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(word in sem_text for word in ["Logout", "Borrow", "Library", "Search", "Return", "Available"]), \
        f"TC-12: UI did not switch to English. Got: {sem_text[:200]}"
