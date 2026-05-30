from pages.base_page import BasePage
from config.settings import COORDS


class AccountsPage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
        self.click_coord(COORDS["sidebar"]["accounts"])
        self.wait_ms(2_000)

        result = []
        for i, coord in enumerate(COORDS["accounts_tabs"], start=1):
            name = f"Accounts / Таб {i}"
            self.tag(name)
            print(name)
            self.click(*coord)
            self.wait_ms(2_500)
            result.append((name, self.screenshot()))
        return result
