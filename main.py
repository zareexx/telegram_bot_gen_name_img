import requests
import threading
import os
from tqdm import tqdm

# Параметры
url = 'https://api.rentyourtoken.org/api/getUsernamesPhotos'
api_token = 'токен'
format = 'text'
threads_count = 5  # Количество потоков
downloads_count = 100  # Количество выгрузок

# Создание папки для изображений, если она не существует
if not os.path.exists('img'):
    os.makedirs('img')

# Создание файла для имен, если он не существует
if not os.path.exists('name.txt'):
    open('name.txt', 'w').close()

# Функция для выгрузки данных
def download_data(pbar):
    params = {
        'api_token': api_token,
        'format': format
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.text.split('\n')
        for item in data:
            if item:
                name, image_url = item.split('|')
                with open('name.txt', 'a') as f:
                    f.write(name + '\n')
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with open(f'img/{name}.jpg', 'wb') as f:
                        f.write(image_response.content)
                else:
                    print(f'Ошибка при загрузке изображения: {image_url}')
                pbar.update(1)
    else:
        print(f'Ошибка при запросе данных: {url}')

# Функция для запуска потоков
def start_threads(count, pbar):
    threads = []
    for _ in range(count):
        thread = threading.Thread(target=download_data, args=(pbar,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

# Запуск потоков
pbar = tqdm(total=downloads_count, desc='Выгрузка данных')
for _ in range(downloads_count // threads_count):
    start_threads(threads_count, pbar)
pbar.close()
