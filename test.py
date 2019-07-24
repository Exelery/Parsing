with open("proxies.txt", 'r') as f:
    answer = list(f.read().split())
    proxies = {}
   # for i in answer:
   #     key = 'https' if 'https' in i else 'http'
   #     print(key)
    #    proxies[key] = i
print(proxies)