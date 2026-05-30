from pages.base_page import BasePage
from config.settings import COORDS

_TAB_NAMES = ["Teams", "Info", "Spending Policies"]


class CompanyPage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
        self.tag("Company / Members")
        print("Company / Members")
        self.click_coord(COORDS["sidebar"]["company"])
        self.wait_ms(2_000)
        result = [("Company / Members", self.screenshot())]

        for name, coord in zip(_TAB_NAMES, COORDS["company_tabs"]):
            self.tag(f"Company / {name}")
            print(f"Company / {name}")
            self.click(*coord)
            self.wait_ms(2_500)
            result.append((f"Company / {name}", self.screenshot()))
        return result
