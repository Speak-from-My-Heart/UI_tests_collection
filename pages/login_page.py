"""
LoginPage — логин в приложение.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class LoginPage(BasePage):
    def __init__(self, bm, collector, site: dict):  # ← добавить site
        super().__init__(bm, collector)
        self.site = site

    def open(self) -> None:
        self.tag("Login")
        self.page.goto(self.site["url"])
        self.page.wait_for_selector("flutter-view", timeout=45_000)
        self.wait_network(timeout=30_000)
        self.wait_ms(3_000)
        print("Страница логина загружена")

    def login(self) -> None:
        """Вводит email, пароль и нажимает Submit."""
        # Email
        self.click(*COORDS["login_email"])
        self.page.keyboard.type(self.site["email"])
        self.page.keyboard.press("Tab")
        self.wait_ms(1_000)

        # Password
        self.page.keyboard.type(self.site["password"])

        # Submit
        self.click(*COORDS["login_submit"])
        self.wait_network(timeout=30_000)
        self.wait_ms(2_000)
        print("Логин выполнен")
