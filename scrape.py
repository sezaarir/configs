import requests
from bs4 import BeautifulSoup
import re

# لیست کانال‌ها رو اینجا اضافه کن (بدون @)
CHANNELS = [
    'prrofile_purple',          # کانال اول (مثال)
    'v2city',         # کانال دوم
    '',          # کانال سوم - هر چند تا می‌خوای اضافه کن
    'نام_کانال_چهارم',
    # اضافه کن ...
]

output_lines = []

for channel in CHANNELS:
    url = f'https://t.me/s/{channel}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        messages = soup.find_all('div', class_='tgme_widget_message_text')

        output_lines.append(f"\n=== کانال: @{channel} ===\n")

        for msg in messages:
            text = msg.get_text(separator='\n', strip=True)
            if re.search(r'(vmess|vless|trojan|ss)://', text):
                output_lines.append("--- پیام جدید ---")
                output_lines.append(text)  # متن کامل بدون کوتاه کردن
                output_lines.append("")

        print(f"کانال {channel} پردازش شد - {len(messages)} پیام بررسی شد")

    except Exception as e:
        print(f"خطا در کانال {channel}: {str(e)}")
        output_lines.append(f"--- خطا در کانال @{channel}: {str(e)} ---")

# ذخیره در فایل
with open('all_configs.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"کل خروجی نوشته شد: {len(output_lines)} خط")
