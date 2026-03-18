import requests
import os

def send_to_telegram(text):
    token = os.getenv('TG_TOKEN')          # из GitHub Secrets
    chat_id = os.getenv('TG_CHAT_ID')      # из GitHub Secrets
    
    if not token or not chat_id:
        print("Ошибка: TG_TOKEN или TG_CHAT_ID не заданы!")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"   # опционально: чтобы жирный, курсив и т.д. работали
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Сообщение отправлено в Telegram!")
        else:
            print("Ошибка отправки:", response.text)
    except Exception as e:
        print("Исключение при отправке в TG:", e)

# Пример использования в конце твоего скрипта:
report = """
*Отчёт за сегодня:*

Успешно обработано: 42 записи  
Ошибок: 0  
Время выполнения: 14 сек
"""
send_to_telegram(report)