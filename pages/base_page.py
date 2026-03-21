"""
BasePage — общий родитель для всех страниц.

Хранит ссылки на page, browser_manager и error_collector.
Предоставляет удобные методы: navigate, click_coord, screenshot, wait.
"""

import time
from playwright.sync_api import Page
from core.browser import BrowserManager
from core.error_collector import ErrorCollector


class BasePage:
    def __init__(self, bm: BrowserManager, collector: ErrorCollector):
        self.bm        = bm
        self.page: Page = bm.page
        self.collector  = collector

    # ── Навигация ────────────────────────────────────────────────────────────

    def wait_network(self, timeout: int = 30_000) -> None:
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_ms(self, ms: int) -> None:
        self.page.wait_for_timeout(ms)

    # ── Клик по координатам ──────────────────────────────────────────────────

    def click(self, x: int, y: int) -> None:
        """Клик с масштабированием под реальный viewport."""
        self.bm.click(x, y)

    def click_coord(self, coord: tuple[int, int]) -> None:
        self.click(*coord)

    # ── Скриншот ─────────────────────────────────────────────────────────────

    def screenshot(self) -> bytes:
        """
        Перед скриншотом всегда ждём networkidle + 2.5 сек сверху.
        Flutter-приложения часто продолжают рендерить после networkidle,
        поэтому перестраховываемся дополнительной паузой.
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass  # если networkidle не пришёл за 15 сек — всё равно делаем скрин
        self.wait_ms(2_500)
        return self.page.screenshot(full_page=True)

    # ── Тег для коллектора ───────────────────────────────────────────────────

    def tag(self, name: str) -> None:
        """Устанавливает тег страницы — все последующие ошибки будут под ним."""
        self.collector.set_page_tag(name)
