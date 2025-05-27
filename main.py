import requests
from bs4 import BeautifulSoup
import time
import random

session = requests.Session()
session.headers.update({
    'User-Agent': random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'
    ])
})

time.sleep(random.uniform(1, 3))

main_url = 'https://www.mibei77.com/'
main_resp = session.get(main_url, timeout=10)
main_resp.encoding = main_resp.apparent_encoding
main_soup = BeautifulSoup(main_resp.text, 'html.parser')

entry_div = main_soup.find('div', class_='entry-content')
if not entry_div:
    print("未找到 entry-content 区块")
    exit()

first_a = entry_div.find('a')
if not first_a or 'href' not in first_a.attrs:
    print("未找到详情页链接")
    exit()

detail_url = first_a['href']
print("详情页链接:", detail_url)

time.sleep(random.uniform(1, 2))
detail_resp = session.get(detail_url, timeout=10)
detail_resp.encoding = detail_resp.apparent_encoding
detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')

p_tags = detail_soup.find_all('p')
sub_link = None
for i in range(len(p_tags) - 1):
    if 'v2ray订阅链接' in p_tags[i].text:
        sub_link = p_tags[i + 1].text.strip()
        break

if not sub_link:
    print("未提取到订阅链接")
    exit()

print("订阅链接:", sub_link)

time.sleep(random.uniform(1, 2))
sub_resp = session.get(sub_link, timeout=20)
if sub_resp.status_code == 200:
    # 直接写入当前目录下的 sub.txt
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(sub_resp.text)
    print("订阅内容已保存到 sub.txt")
else:
    print("获取订阅内容失败，状态码:", sub_resp.status_code)
