"""
monitor.py — главный файл запуска.

Здесь только оркестрация: создаём объекты, обходим страницы,
собираем скриншоты, отправляем отчёт ТОЛЬКО если есть ошибки.

Локально:   python monitor.py
В CI:       python monitor.py  (креды приходят из GitHub Secrets через env:)
"""

import argparse
from config.settings import SITES
from core.browser import BrowserManager
from core.error_collector import ErrorCollector
from notifications.telegram_notifier import TelegramNotifier
from reports.report_builder import ReportBuilder

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.accounts_page import AccountsPage
from pages.cards_page import CardsPage
from pages.payments_page import PaymentsPage
from pages.refunds_page import RefundsPage
from pages.top_ups_page import TopUpsPage
from pages.balance_summary_page import BalanceSummaryPage
from pages.company_page import CompanyPage
from pages.profile_page import ProfilePage


def run_monitor(headless: bool = True, screenshots_mode: bool = False) -> None:
    notifier = TelegramNotifier()

    for site in SITES:
        print(f"\n{'='*40}\nЗапуск для: {site['name']}\n{'='*40}")

        collector   = ErrorCollector()
        screenshots = []

        with BrowserManager(headless=headless) as bm:
            bm.page.on("response", collector.on_response)

            login = LoginPage(bm, collector, site)   # ← передаём site
            login.open()
            login.login()
            screenshots.append(("После логина", login.screenshot()))

            # ── 2. Home / Deposit ─────────────────────────────────────────────────
            home = HomePage(bm, collector)
            home.visit()
            screenshots.append(("Home / Deposit", home.screenshot()))

            # ── 3. Accounts ───────────────────────────────────────────────────────
            accounts = AccountsPage(bm, collector)
            screenshots.extend(accounts.visit())

            # ── 4. Cards ──────────────────────────────────────────────────────────
            cards = CardsPage(bm, collector)
            cards.visit()
            screenshots.append(("Cards", cards.screenshot()))

            # ── 5. Payments ───────────────────────────────────────────────────────
            payments = PaymentsPage(bm, collector)
            payments.visit()
            screenshots.append(("Payments", payments.screenshot()))

            # ── 6. Refunds ────────────────────────────────────────────────────────
            refunds = RefundsPage(bm, collector)
            refunds.visit()
            screenshots.append(("Refunds", refunds.screenshot()))

            # ── 7. Top Ups ────────────────────────────────────────────────────────
            top_ups = TopUpsPage(bm, collector)
            top_ups.visit()
            screenshots.append(("Top Ups", top_ups.screenshot()))

            # ── 8. Balance Summary ────────────────────────────────────────────────
            balance = BalanceSummaryPage(bm, collector)
            balance.visit()
            screenshots.append(("Balance Summary", balance.screenshot()))

            # ── 9. Company ────────────────────────────────────────────────────────
            company = CompanyPage(bm, collector)
            screenshots.extend(company.visit())

            # ── 10. Profile ───────────────────────────────────────────────────────
            profile = ProfilePage(bm, collector)
            screenshots.extend(profile.visit())

            report = ReportBuilder(collector, site["name"])

            if screenshots_mode:
                print(f"[{site['name']}] Режим выгрузки скринов")
                notifier.send_screenshots_report(site["name"], screenshots)
            elif report.has_errors():
                print(f"[{site['name']}] Найдено ошибок: {collector.total()}")
                notifier.send_report_with_screenshots(report.build(), screenshots)
            else:
                print(f"[{site['name']}] Ошибок не найдено ✅")
                notifier.send_text(report.build_ok_message())

    # ── Отчёт ─────────────────────────────────────────────────────────────────

    print("Мониторинг завершён")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show",        action="store_true", help="видимый браузер (для отладки)")
    parser.add_argument("--screenshots", action="store_true", help="тестовая выгрузка скринов в TG")
    args = parser.parse_args()
    run_monitor(headless=not args.show, screenshots_mode=args.screenshots)

#смотреть координаты document.addEventListener('mousemove', e => console.log(`X: ${e.clientX}, Y: ${e.clientY}`));
