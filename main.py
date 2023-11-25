import requests
from bs4 import BeautifulSoup
import lxml
import base64

def get_free_proxies():

    cookies = {
    '_ga': 'GA1.1.783910457.1700902641',
    'fp': '713f323ac4ddd66f5b8433057824a9b4',
    '_ga_FS4ESHM7K5': 'GS1.1.1700902641.1.1.1700902659.0.0.0',
    }

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'uk,uk-UA;q=0.9,en;q=0.8,pl;q=0.7,ru;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga=GA1.1.783910457.1700902641; fp=713f323ac4ddd66f5b8433057824a9b4; _ga_FS4ESHM7K5=GS1.1.1700902641.1.1.1700902659.0.0.0',
    'DNT': '1',
    'Referer': 'http://free-proxy.cz/en/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    s = requests.Session()
    response = s.get('http://free-proxy.cz/en/proxylist/country/UA/all/ping/all', cookies=cookies, headers=headers)

    # with open('proxy.html', 'w') as file:
    #     file.write(response.text)

    # with open('proxy.html') as file:
    #     src = file.read()

    soup = BeautifulSoup(response.text, 'lxml')
    countries = soup.find('select', id='frmsearchFilter-country').find_all('option')

    print('[INFO] aviable countries:')
    
    for c in countries:
        short_name = c.get('value')
        name = c.text.split('(')[0].strip()
        print(f'{short_name} <--> {name}')

    select_country = input('[INFO] select country: ')
    url = f'http://free-proxy.cz/en/proxylist/country/{select_country}/all/ping/all'
    print(url)
    print('[INFO] getting proxies...')

    response = s.get(url, cookies=cookies, headers=headers)
    ip_list = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        table_trs = soup.find('table', id='proxy_list').find('tbody').find_all('tr')
        for tr in table_trs:

            try:
                ip = tr.find('td').find('script').text
            except Exception as ex:
                print(ex)
                continue

            if ip:
                ip = base64.b64decode(ip.split('"')[1]).decode('utf-8')
                port = tr.find('span', class_='fport').text
                print(f'[+] {ip}:{port}')
                ip_list.append(f'{ip}:{port}')
            else:
                continue

        with open(f'{select_country}.ip_list.txt', 'w') as file:
            file.writelines(f'{select_country} - {ip}\n' for ip in ip_list)
        
        print(f'[INFO] {len(ip_list)} proxies saved to ip_list.txt')
    else:
        print(f'[ERROR] {response.status_code}')

def main():
    get_free_proxies()

if __name__ == "__main__":
    main()