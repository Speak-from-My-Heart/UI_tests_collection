from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://app.elibrium.io/auth/login"
VIEWPORT = {"width": 1100, "height": 700}
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
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )
        context = browser.new_context(viewport = VIEWPORT)
        page = context.new_page()
        all_errors = []

        def global_on_response(response):
            status = response.status
            if 204 <= status <= 599:  
                all_errors.append({
                    'status': status,
                    'url': response.url,
                    'method': response.request.method,
                    'page_url': page.url 
                })
                print(f"RESPONSE CAUGHT: {response.request.method} {response.url} → {status}")  # debug

        page.on("response", global_on_response)

        def print_caught_errors(page_name="Текущая страница"):
            current_url = page.url
            page_errors = [e for e in all_errors if e['page_url'] == current_url]

            print(f"\nСтатусы ошибок на '{page_name}' ({current_url}):")
            if page_errors:
                for e in page_errors:
                    print(f"  {e['method']} {e['url']} → {e['status']}")
                print(f"Всего: {len(page_errors)}")
            else:
                print("  Нет плохих статусов на этой странице (или они пойманы раньше)")

        page.goto(BASE_URL, wait_until="networkidle", timeout=45000)
        page.wait_for_selector(
            'flutter-view',
            timeout=45000
        )
        print("страница готова")
        page.wait_for_timeout(3000)

        print_caught_errors(page_name="Страница логина")

        # Authorisation
        page.mouse.click(x=700, y=270)
        page.keyboard.type(CREDENTIALS["email"], delay=10)
        page.keyboard.press("Tab")
        page.wait_for_timeout(1000)
        page.keyboard.type(CREDENTIALS["password"], delay=10)
        page.mouse.click(x=800, y=530)

        # Home
        page.wait_for_load_state("networkidle", timeout=20000)
        page.wait_for_timeout(1000)
        page.mouse.click(x=950, y=160)
        page.wait_for_timeout(3000)
        page.mouse.click(x=1020, y=45)
        page.wait_for_timeout(1000)
        print_caught_errors(page_name="Страница Home")

        # Accounts
        print("Accounts")
        page.mouse.click(*COORDS["sidebar"]["accounts"]) #x=150, y=210
        page.wait_for_timeout(1000)
        page.mouse.click(x=650, y=50)
        page.wait_for_timeout(1000)
        page.mouse.click(x=850, y=50)
        page.wait_for_timeout(1000)
        print_caught_errors(page_name="Страница Accounts")

        # Cards
        print("Cards")
        page.mouse.click(x=150, y=270)
        page.wait_for_timeout(1000)
        page.mouse.click(x=870, y=50)
        page.wait_for_timeout(1000)
        page.mouse.click(x=1020, y=45)
        page.wait_for_timeout(1000)
        print_caught_errors(page_name="Страница Cards")

        # Payments
        print("Payments")
        page.mouse.click(x=150, y=350)
        page.wait_for_timeout(1000)

        #Refunds
        print("Refunds")
        page.mouse.click(x=150, y=400)
        page.wait_for_timeout(1000)

        # Top ups
        page.mouse.move(150, 320)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(100)
        page.mouse.click(x=150, y=320)
        page.wait_for_timeout(1000)
        page.mouse.click(x=950, y=160)
        page.wait_for_timeout(3000)
        page.mouse.click(x=1020, y=45)
        page.wait_for_timeout(1000)

        # Balance summary
        page.mouse.move(150, 320)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(1000)
        page.mouse.click(x=150, y=400)
        page.wait_for_timeout(3000)


        # Браузер остаётся открытым до твоего Ctrl+C или закрытия окна
        print("Нажми Ctrl+C в терминале для завершения скрипта.")

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            print("Завершаем работу...")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()


# document.onmousemove = e => {
#   console.clear();
#   console.log(`X: ${e.clientX}   Y: ${e.clientY}   (pageX: ${e.pageX}, pageY: ${e.pageY})`);
# };