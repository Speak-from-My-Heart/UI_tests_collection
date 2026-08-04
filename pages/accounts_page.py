from pages.base_page import BasePage
from config.settings import COORDS

_TAB_NAMES = ["Transfers", "Balance History"]
_MAX_RETRIES = 3


class AccountsPage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
        self.click_coord(COORDS["sidebar"]["accounts"])
        self.wait_ms(10_000)

        _tab_wait = {"Balance History": 24_000}

        result = []
        for name, coord in zip(_TAB_NAMES, COORDS["accounts_tabs"]):
            tag = f"Accounts / {name}"
            self.tag(tag)
            print(tag)

            for attempt in range(_MAX_RETRIES):
                self.click(*coord)
                self.wait_ms(4_000)
                self.wait_network(timeout=90_000)
                self.wait_ms(_tab_wait.get(name, 6_000))

                if not self.collector.errors_for_tag(tag) or attempt == _MAX_RETRIES - 1:
                    break

                print(f"{tag}: ошибки на попытке {attempt + 1}, ретрай...")
                self.collector.clear_tag(tag)

            result.append((tag, self.screenshot()))
        return result
