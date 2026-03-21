"""
BalanceSummaryPage — раздел Balance Summary.
Требует прокрутки сайдбара вниз перед кликом.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class BalanceSummaryPage(BasePage):

    def visit(self) -> None:
        self.tag("Balance Summary")
        print("Balance Summary")
        self.bm.scroll_sidebar(400)
        self.wait_ms(1_000)
        self.click_coord(COORDS["sidebar"]["balance_summary"])
        self.wait_ms(4_000)
