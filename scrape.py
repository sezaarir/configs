import requests
from bs4 import BeautifulSoup
import re

# نام کانال رو اینجا بگذار (بدون @)
CHANNEL = 'prrofile_purple'  # مثلاً V2rayCollector یا هر کانالی که داری

url = f'https://t.me/s/{CHANNEL}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()  # اگر خطا بود، raise کن
    soup = BeautifulSoup(response.text, 'html.parser')

    messages = soup.find_all('div', class_='tgme_widget_message_text')
    output_lines = []

    for msg in messages:
        text = msg.get_text(separator='\n', strip=True)
        # اگر حداقل یک لینک کانفیگ داشت
        if re.search(r'(vmess|vless|trojan|ss)://', text):
            # متن کامل پیام رو اضافه کن (بدون کوتاه کردن)
            output_lines.append("--- پیام جدید ---")
            output_lines.append(text)
            output_lines.append("")  # خط خالی برای جداسازی بهتر

    if output_lines:
        with open('all_configs.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        print(f"نوشته شد: {len(output_lines)} خط - کانفیگ‌ها کامل ذخیره شدند")
    else:
        print("هیچ کانفیگی پیدا نشد")

except Exception as e:
    print(f"خطا در scrape: {str(e)}")
