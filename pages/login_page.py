"""
LoginPage — логин в приложение.
"""

from pages.base_page import BasePage
from config.settings import BASE_URL, CREDENTIALS, COORDS


class LoginPage(BasePage):

    def open(self) -> None:
        self.tag("Login")
        self.page.goto(BASE_URL, wait_until="networkidle", timeout=45_000)
        self.page.wait_for_selector("flutter-view", timeout=45_000)
        self.wait_network(timeout=30_000)
        self.wait_ms(3_000)
        print("Страница логина загружена")

    def login(self) -> None:
        """Вводит email, пароль и нажимает Submit."""
        # Email
        self.click(*COORDS["login_email"])
        self.page.keyboard.type(CREDENTIALS["email"], delay=10)
        self.page.keyboard.press("Tab")
        self.wait_ms(1_000)

        # Password
        self.page.keyboard.type(CREDENTIALS["password"], delay=10)

        # Submit
        self.click(*COORDS["login_submit"])
        self.wait_network(timeout=30_000)
        self.wait_ms(2_000)
        print("Логин выполнен")
