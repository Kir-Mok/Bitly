import os
import argparse
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
from pathlib import Path


def shorten_link(url, headers):
    api_url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {
        'long_url': url
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()['id']


def count_clicks(short_link, headers):
    parsed_link = urlparse(short_link)

    api_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary'.format(
        parsed_link.netloc, parsed_link.path)

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(link, headers):
    parsed_link = urlparse(link)

    api_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}'.format(
        parsed_link.netloc, parsed_link.path)

    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    secret = os.environ['API']

    headers = {
        'Authorization': secret
    }

    parser = argparse.ArgumentParser(description='Получает клики по битлинку')
    parser.add_argument('url', help='Ссылка в дальнейшем будет сокращена')
    args = parser.parse_args()

    input_link = args.url

    if is_bitlink(input_link, headers):
        try:
            clicks_count = count_clicks(input_link, headers)
            print(clicks_count)
        except requests.exceptions.HTTPError:
            print('Невозможно подсчитать клики')
    else:
        try:
            short_link = shorten_link(input_link, headers)
            print(short_link)
        except requests.exceptions.HTTPError:
            print('Невозможная ссылка')


if __name__ == '__main__':
    main()
