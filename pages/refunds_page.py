"""
RefundsPage — раздел Refunds.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class RefundsPage(BasePage):

    def visit(self) -> None:
        self.tag("Refunds")
        print("Refunds")
        self.click_coord(COORDS["sidebar"]["refunds"])
        self.wait_ms(2_000)
