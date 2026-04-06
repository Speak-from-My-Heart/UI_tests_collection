"""
ErrorCollector — перехватывает HTTP-ответы от Playwright и хранит ошибки.

Главное отличие от оригинала:
  Вместо сохранения page.url (который может быть устаревшим на момент
  асинхронного ответа), мы используем явные теги страниц.
  Перед навигацией вызываем collector.set_page_tag("Accounts"),
  и все ответы, пришедшие после этого, будут помечены этим тегом.
"""

from config.settings import ERROR_STATUS_THRESHOLD, IGNORE_URL_PATTERNS


class ErrorCollector:
    def __init__(self):
        self._errors: list[dict] = []
        self._current_tag: str = "unknown"

    # ── Публичный API ────────────────────────────────────────────────────────

    def set_page_tag(self, tag: str) -> None:
        """Вызывай перед каждой навигацией, чтобы ошибки получили правильный тег."""
        self._current_tag = tag

    def on_response(self, response) -> None:
        """Передай этот метод в page.on('response', collector.on_response)."""
        status = response.status
        if status >= ERROR_STATUS_THRESHOLD:
            # игнорируем известные незначимые ошибки
            if any(p in response.url for p in IGNORE_URL_PATTERNS):
                return
            entry = {
                "status": status,
                "url":    response.url,
                "method": response.request.method,
                "tag":    self._current_tag,
            }
            self._errors.append(entry)
            print(f"[{self._current_tag}] {entry['method']} {entry['url']} → {status}")

    def errors_for_tag(self, tag: str) -> list[dict]:
        """Возвращает все ошибки, помеченные данным тегом."""
        return [e for e in self._errors if e["tag"] == tag]

    def all_errors(self) -> list[dict]:
        return list(self._errors)

    def total(self) -> int:
        return len(self._errors)

    def collector_threshold_label(self) -> str:
        """Подпись к порогу — чтобы в отчёте было понятно, что считается."""
        return f"{ERROR_STATUS_THRESHOLD}+"

    def format_section(self, tag: str) -> str:
        """
        Форматирует блок отчёта для одного раздела.
        Возвращает строку — добавляй в общий report.
        """
        errors = self.errors_for_tag(tag)
        lines = [f"\n*{tag}*"]
        if errors:
            for e in errors:
                lines.append(f"  {e['method']} {e['url']} → {e['status']}")
            lines.append(f"Ошибок: {len(errors)}")
        else:
            lines.append("Ошибок 4xx/5xx не обнаружено ✅")
        return "\n".join(lines)
