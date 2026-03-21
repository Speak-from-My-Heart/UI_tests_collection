"""
BrowserManager — запускает Playwright, создаёт контекст и страницу.
Также умеет масштабировать координаты под реальный viewport.
"""

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from config.settings import VIEWPORT, SLOW_MO_MS, BASE_W, BASE_H


class BrowserManager:
    def __init__(self, headless: bool = True):
        self._headless = headless
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self.page: Page | None = None

    # ── Контекст-менеджер ────────────────────────────────────────────────────

    def __enter__(self) -> "BrowserManager":
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self._headless,
            slow_mo=SLOW_MO_MS,
        )
        self._context = self._browser.new_context(viewport=VIEWPORT)
        self.page = self._context.new_page()
        return self

    def __exit__(self, *_):
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    # ── Масштабирование координат ────────────────────────────────────────────

    def scale(self, x: int, y: int) -> tuple[int, int]:
        """
        Пересчитывает координаты из базового разрешения (BASE_W × BASE_H)
        в реальный viewport. Защищает от поломки при смене разрешения.
        """
        vp = self.page.viewport_size or VIEWPORT
        sx = int(x * vp["width"]  / BASE_W)
        sy = int(y * vp["height"] / BASE_H)
        return sx, sy

    def click(self, x: int, y: int) -> None:
        sx, sy = self.scale(x, y)
        self.page.mouse.click(sx, sy)

    def scroll_sidebar(self, delta_y: int = 400) -> None:
        """Прокручивает сайдбар вниз (координата X = 150 — левая панель)."""
        sx, _ = self.scale(150, 320)
        self.page.mouse.move(sx, 320)
        self.page.mouse.wheel(0, delta_y)
