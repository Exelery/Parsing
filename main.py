import requests
import json
from proxy_load import main

main()
with open("proxies.txt", 'r') as f:
    proxies = list(f.read().split())



find = 'hi'
headers ={'authority': 'yandex.ru',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9,ro;q=0.8',
            'referer': 'https://yandex.ru/',
            'x-requested-with': 'XMLHttpRequest',
}

session = requests.Session()
answer = session.get('https://yandex.ru/suggest/suggest-ya.cgi?&uil=ru&v=4&bemjson=1&part={}'.format(find),
                      headers=headers, proxies=proxies)

suggest_data = json.loads(answer.text)
suggests = []
for answer in suggest_data[1]:
    suggests.append(answer[1])

print(suggests)
