"""
PaymentsPage — раздел Payments.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class PaymentsPage(BasePage):

    def visit(self) -> None:
        self.tag("Payments")
        print("Payments")
        self.click_coord(COORDS["sidebar"]["payments"])
        self.wait_ms(2_000)
