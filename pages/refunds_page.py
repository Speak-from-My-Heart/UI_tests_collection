"""
RefundsPage — раздел Refunds.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class RefundsPage(BasePage):

    def visit(self) -> None:
        self.tag("Refunds")
        print("Refunds")
        self.bm.scroll_sidebar(60)
        self.wait_ms(500)
        self.click_coord(COORDS["sidebar"]["refunds"])
        self.wait_ms(2_000)
