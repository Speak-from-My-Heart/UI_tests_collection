"""
AccountsPage — раздел Accounts + клик по табам.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class AccountsPage(BasePage):

    def visit(self) -> None:
        self.tag("Accounts")
        print("Accounts")
        self.click_coord(COORDS["sidebar"]["accounts"])
        self.wait_ms(2_000)

        for coord in COORDS["accounts_tabs"]:
            self.click(*coord)
            self.wait_ms(2_500)
