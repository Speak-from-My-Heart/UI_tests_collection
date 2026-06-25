"""
ReportBuilder — собирает финальный текст отчёта из секций ErrorCollector.
"""

import time
from core.error_collector import ErrorCollector


class ReportBuilder:
    # Все разделы в порядке обхода (должны совпадать с тегами в pages/)
    SECTIONS = [
        "Login",
        "Home / Deposit",
        "Accounts / Transfers",
        "Accounts / Balance History",
        "Cards",
        "Cards / Card Credentials",
        "Payments",
        "Refunds",
        "Top Ups",
        "Balance Summary",
        "Company / Members",
        "Company / Teams",
        "Company / Info",
        "Company / Spending Policies",
        "Profile / Account",
        "Profile / Notifications",
        "Profile / API",
    ]

    def __init__(self, collector: ErrorCollector, site_name: str = ""):
        self.collector  = collector
        self.site_name  = site_name

    def build(self) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        lines = [f"*Отчёт проверки {self.site_name} {timestamp}*\n"]

        for section in self.SECTIONS:
            errors = self.collector.errors_for_tag(section)
            if errors:
                lines.append(self.collector.format_section(section))

        lines.append(f"\n*Всего ошибок {self.collector.collector_threshold_label()}: {self.collector.total()}*")
        return "\n".join(lines)

    def build_ok_message(self) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        icon = "🟡" if self.site_name == "Axiona" else "✅"
        return f"{icon} *{self.site_name} ({timestamp}) — ошибок нет*"

    def has_errors(self) -> bool:
        return self.collector.total() > 0
