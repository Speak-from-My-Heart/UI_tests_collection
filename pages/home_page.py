"""
HomePage — главная страница после логина (Deposit и т.д.)
"""

from pages.base_page import BasePage
from config.settings import COORDS


class HomePage(BasePage):

    def visit(self) -> None:
        self.tag("Home / Deposit")
        print("Home → Make a deposit")
        self.click_coord(COORDS["header"]["make_a_deposit"])
        self.wait_ms(3_000)
        self.click_coord(COORDS["header"]["close"])
        self.wait_ms(1_500)
