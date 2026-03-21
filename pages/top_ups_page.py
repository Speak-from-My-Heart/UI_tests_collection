"""
TopUpsPage — раздел Top Ups.
Требует прокрутки сайдбара вниз перед кликом.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class TopUpsPage(BasePage):

    def visit(self) -> None:
        self.tag("Top Ups")
        print("Top Ups")
        self.bm.scroll_sidebar(400)
        self.wait_ms(500)
        self.click_coord(COORDS["sidebar"]["top_ups"])
        self.wait_ms(2_000)
        # Deposit модалка, которая открывается на этой странице
        self.click_coord(COORDS["header"]["make_a_deposit"])
        self.wait_ms(3_000)
        self.click_coord(COORDS["header"]["close"])
        self.wait_ms(1_000)
