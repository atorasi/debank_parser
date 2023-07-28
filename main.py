import requests
import pyuseragents
import json

from config import NEED_TO_SAVE, POST_NUMBER, LAST_POST_NUMBER, TOKEN, SEND_TO, LINK_TO_CHANGE_PROXY, MOBILE_PROXY


def change_proxy_ip():
    r = requests.get(LINK_TO_CHANGE_PROXY)

def send_telegram_message(token: str, chat_id :int, text: str):
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    data = {'chat_id': chat_id, 'text': text}

    r = requests.post(url, data=data)

def main(post_number: int) -> int:
    headers = {
        'authority': 'api.debank.com',
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://debank.com',
        'referer': 'https://debank.com/',
        'source': 'web',
        'user-agent': pyuseragents.random(),
    }
    
    params = {
        'id': post_number
    }
    
    proxy_dict = {
        "http": f"http://{MOBILE_PROXY}",
        "https": f"http://{MOBILE_PROXY}"
    }
    
    
    url = f'https://api.debank.com/article'
    r = requests.get(url, headers=headers, params=params, proxies=proxy_dict)
    if r.status_code == 429: 
        print('Too many requests.')
        return 0
    
    json_data = json.loads(r.text)
    if json_data['data']['article']['draw']:
        if NEED_TO_SAVE:
            with open('draws.txt', 'a') as file:
                file.write(f'https://debank.com/stream/{post_number}\n')
                print(f'NEW DRAW | {POST_NUMBER}')
            
        send_telegram_message(TOKEN, SEND_TO, f'NEW DRAW  - https://debank.com/stream/{post_number}')
        return 1
                
    print(f'No Draw | {POST_NUMBER}')        
    return 1 
    
    

if __name__ == '__main__':
    while POST_NUMBER <= LAST_POST_NUMBER:
        change_proxy_ip()
        
        if main(POST_NUMBER) != 0:
            POST_NUMBER += 1
            

            
