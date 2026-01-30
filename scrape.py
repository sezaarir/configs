import requests
from bs4 import BeautifulSoup
import re

CHANNEL = 'prrofile_purple'  # بدون @ بگذار

url = f'https://t.me/s/{CHANNEL}'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    messages = soup.find_all('div', class_='tgme_widget_message_text')
    lines = []

    for msg in messages:
        text = msg.get_text(separator='\n', strip=True)
        links = re.findall(r'(vmess|vless|trojan|ss)://[^\s<"]+', text)
        if links:
            lines.append(f"پیام جدید:")
            lines.append(text[:200] + '...' if len(text) > 200 else text)  # کوتاه برای حجم کم
            for link in links:
                lines.append(link)
            lines.append("---")

    with open('all_configs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"نوشته شد: {len(lines)} خط")

except Exception as e:
    print(f"خطا: {e}")
