from datetime import datetime
from functools import wraps
import requests
from bs4 import BeautifulSoup


def log_decorator(old_function):
    '''Декоратор - логгер.
    Он записывает в файл дату и время вызова функции,
    имя функции, аргументы, с которыми вызвалась и возвращаемое значение.'''
    @wraps(old_function)
    def new_function(*args, **kwargs):
        date_time = datetime.now()
        function_name = old_function.__name__
        result = old_function(*args, **kwargs)
        with open('log_decorator.log', 'w', encoding='utf-8') as file:
            file.write(f'Дата и время: {date_time}\n'
                        f'Имя функции: {function_name}\n'
                        f'Аргументы: {args, kwargs}\n'
                        f'Результат: {result}\n')
        return result
    return new_function


def logs_path(path):
    '''Декоратор с параметром – путь к логам.'''
    def log_decorator(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            date_time = datetime.now()
            function_name = old_function.__name__
            result = old_function(*args, **kwargs)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(f'Дата и время: {date_time}\n'
                        f'Имя функции: {function_name}\n'
                        f'Аргументы: {args, kwargs}\n'
                        f'Результат: {result}\n')
            return result
        return new_function
    return log_decorator

@log_decorator
@logs_path('logs_path.log')
def scrapping_habr(KEYWORD):
    '''Функция по поиску интересующих нас статей на Хабре по ключевому слову'''
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'
    HEADERS = {
        'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'sec-ch-ua-mobile': '?0'
    }
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("article")

    for article in articles:
        hubs = article.find_all(class_='tm-article-snippet__hubs-item-link')
        hubs = set(hub.find('span').text for hub in hubs)
        preview_text = article.find('div').text
        date = article.find('time').text
        title = article.find(class_='tm-article-snippet__title-link').find('span').text
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        url_post = base_url + href

        if (KEYWORD.lower() in title.lower()) or (KEYWORD.lower() in hubs) or (KEYWORD.lower() in preview_text.lower()):
            res = f'Дата: {date} - Заголовок: {title} - Ссылка: {url_post}'
    return res

if __name__ == '__main__':
    scrapping_habr('Python')
