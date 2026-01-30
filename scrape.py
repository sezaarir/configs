import requests
from bs4 import BeautifulSoup
import re

CHANNEL = 'نام_کانالت_بدون_@'  # مثلاً 'prrofile_purple' یا هر کانال

url = f'https://t.me/s/{CHANNEL}'
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    messages = soup.find_all('div', class_='tgme_widget_message_text')
    output_lines = []

    for msg in messages:
        text = msg.get_text(separator='\n', strip=True)
        if re.search(r'(vmess|vless|trojan|ss)://', text):
            output_lines.append("--- پیام جدید ---")
            output_lines.append(text)
            output_lines.append("")  # خط خالی برای جداسازی

    with open('all_configs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"نوشته شد: {len(output_lines)} خط")

except Exception as e:
    print(f"خطا: {e}")
