import requests
from bs4 import BeautifulSoup
import re
import json

# ← اینجا نام کانال خودت رو بدون @ بگذار
CHANNEL = 'V2rayCollector'   # مثال: 'proxy_mtproto_ir' یا هر کانال دلخواه

url = f'https://t.me/s/{CHANNEL}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    messages = soup.find_all('div', class_='tgme_widget_message_text')
    configs = []

    for msg in messages:
        text = msg.get_text(separator=' ', strip=True)
        links = re.findall(r'(vmess|vless|trojan|ss)://[^\s<"]+', text)
        for link in links:
            # توضیح کوتاه از ابتدای پیام (حداکثر ۱۰۰ کاراکتر)
            desc = text[:120].strip() + '…' if len(text) > 120 else text.strip()
            configs.append({'link': link, 'desc': desc})

    # ذخیره در فایل
    with open('configs.json', 'w', encoding='utf-8') as f:
        json.dump(configs, f, ensure_ascii=False, indent=2)

    print(f'تعداد کانفیگ استخراج‌شده: {len(configs)}')

except Exception as e:
    print(f'خطا: {str(e)}')
