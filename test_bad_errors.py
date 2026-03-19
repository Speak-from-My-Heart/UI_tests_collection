from playwright.sync_api import sync_playwright
import time
import requests
import os

from dotenv import load_dotenv
load_dotenv()

# ────────────────────────────────────────────────
# Настройки Telegram (берём из переменных окружения)
# ────────────────────────────────────────────────
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

def send_telegram_text(text: str):
    if not TG_TOKEN or not TG_CHAT_ID:
        print("TG_TOKEN или TG_CHAT_ID не заданы → пропускаем отправку в Telegram")
        return

    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print("Текст отправлен в Telegram")
    except Exception as e:
        print(f"Ошибка отправки текста в TG: {e}")


def send_telegram_photo(photo_bytes: bytes, caption: str = ""):
    if not TG_TOKEN or not TG_CHAT_ID:
        print("TG_TOKEN или TG_CHAT_ID не заданы → пропускаем фото")
        return

    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    
    files = {"photo": ("screenshot.png", photo_bytes, "image/png")}
    data = {"chat_id": TG_CHAT_ID}
    if caption:
        data["caption"] = caption
        data["parse_mode"] = "Markdown"

    try:
        r = requests.post(url, files=files, data=data, timeout=15)
        r.raise_for_status()
        print(f"Фото отправлено: {caption}")
    except Exception as e:
        print(f"Ошибка отправки фото в TG: {e}")


# ────────────────────────────────────────────────
# Твои константы (без изменений)
# ────────────────────────────────────────────────

BASE_URL = "https://app.elibrium.io/auth/login"
VIEWPORT = {"width": 1280, "height": 700}
SLOW_MO_MS = 300

CREDENTIALS = {
    "email": "qa+k+brandE@elibrium.io",
    "password": "xIR6eIyuu\\~qU#J8o"  
}

COORDS = {
    "login_email":    (700, 270),
    "login_submit":   (800, 530),
    "sidebar": {
        "accounts":       (150, 210),
        "cards":          (150, 270),
        "payments":       (150, 350),
        "refunds":        (150, 400),
        "top_ups":        (150, 320),
        "balance_summary":(150, 400),   
    },
    "header": {
        "make_a_deposit": (950, 160),
        "close":  (1020, 45),
    }
}


def main():
    all_errors = []
    screenshots = []   # список (название_экрана, байты)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,          # ← в облаке обязательно True!
            slow_mo=SLOW_MO_MS
        )
        context = browser.new_context(viewport=VIEWPORT)
        page = context.new_page()

        def global_on_response(response):
            status = response.status
            if status >= 300:  # чаще всего интересуют именно >=400
                all_errors.append({
                    'status': status,
                    'url': response.url,
                    'method': response.request.method,
                    'page_url': page.url 
                })
                print(f"ERROR RESPONSE: {response.request.method} {response.url} → {status}")

        page.on("response", global_on_response)

        def print_and_collect_errors(page_name="Текущая страница"):
            current_url = page.url
            page_errors = [e for e in all_errors if e['page_url'] == current_url]

            msg = f"\n**{page_name}** ({current_url})\n"
            if page_errors:
                for e in page_errors:
                    msg += f"  {e['method']} {e['url']} → {e['status']}\n"
                msg += f"Всего ошибок: {len(page_errors)}\n"
            else:
                msg += "Ошибок 4xx/5xx на этой странице не обнаружено\n"
            print(msg.strip())
            return msg

        # ─── Логин ───────────────────────────────────────
        page.goto(BASE_URL, wait_until="networkidle", timeout=45000)
        page.wait_for_selector('flutter-view', timeout=45000)
        print("Страница логина загружена")
        page.wait_for_load_state("networkidle", timeout=30000)    # ждём, пока утихнут все XHR
        page.wait_for_timeout(3000)

        page.mouse.click(x=880, y=270)
        page.keyboard.type(CREDENTIALS["email"], delay=10)
        page.keyboard.press("Tab")
        time.sleep(1)
        page.keyboard.type(CREDENTIALS["password"], delay=10)
        page.mouse.click(x=880, y=500)

        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)

        # Скрин после логина
        png_bytes = page.screenshot(full_page=True)
        screenshots.append(("После логина", png_bytes))

        # ─── Home / Deposit ──────────────────────────────
        print("Home → Make a deposit")
        page.mouse.click(*COORDS["header"]["make_a_deposit"])
        time.sleep(3)
        page.mouse.click(*COORDS["header"]["close"])
        time.sleep(1.5)

        err_home = print_and_collect_errors("Home / Deposit")
        screenshots.append(("Home после Deposit", page.screenshot(full_page=True)))

        # ─── Accounts ────────────────────────────────────
        print("Accounts")
        page.mouse.click(*COORDS["sidebar"]["accounts"])
        time.sleep(2)
        page.mouse.click(x=650, y=50)
        time.sleep(1.5)
        page.mouse.click(x=850, y=50)
        time.sleep(1.5)

        err_accounts = print_and_collect_errors("Accounts")
        screenshots.append(("Accounts", page.screenshot(full_page=True)))

        # ─── Cards ───────────────────────────────────────
        print("Cards")
        page.mouse.click(*COORDS["sidebar"]["cards"])
        time.sleep(2)
        page.mouse.click(x=870, y=50)
        time.sleep(1.5)
        page.mouse.click(*COORDS["header"]["close"])
        time.sleep(1)

        err_cards = print_and_collect_errors("Cards")
        screenshots.append(("Cards", page.screenshot(full_page=True)))

        # ─── Payments / Refunds / Top ups / Balance ──────
        # (можно добавить скриншоты и сюда по желанию)

        page.mouse.click(*COORDS["sidebar"]["payments"])
        time.sleep(2)

        page.mouse.click(*COORDS["sidebar"]["refunds"])
        time.sleep(2)

        page.mouse.move(150, 320)
        page.mouse.wheel(0, 400)
        time.sleep(0.5)
        page.mouse.click(*COORDS["sidebar"]["top_ups"])
        time.sleep(2)
        page.mouse.click(*COORDS["header"]["make_a_deposit"])
        time.sleep(3)
        page.mouse.click(*COORDS["header"]["close"])
        time.sleep(1)

        page.mouse.move(150, 320)
        page.mouse.wheel(0, 400)
        time.sleep(1)
        page.mouse.click(*COORDS["sidebar"]["balance_summary"])
        time.sleep(4)

        err_summary = print_and_collect_errors("Balance Summary + другие вкладки")
        screenshots.append(("Balance Summary", page.screenshot(full_page=True)))

        # ─── Финальный отчёт ─────────────────────────────
        report = f"""*Отчёт проверки {time.strftime('%Y-%m-%d %H:%M')}*

**Ошибки по разделам:**

{err_home}
{err_accounts}
{err_cards}
{err_summary}

Всего ошибок 4xx/5xx: {len(all_errors)}
"""

        send_telegram_text(report)

        # Отправляем скриншоты (по одному, чтобы не перегружать)
        for name, png_bytes in screenshots:
            send_telegram_photo(png_bytes, f"Скриншот: **{name}**")
            time.sleep(1.2)   # небольшой интервал, чтобы Telegram не ругался

        print("Скрипт завершён")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()


# document.onmousemove = e => {
#   console.clear();
#   console.log(`X: ${e.clientX}   Y: ${e.clientY}   (pageX: ${e.pageX}, pageY: ${e.pageY})`);
# };1