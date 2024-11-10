from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import request
from http import HTTPMethod
from app.models.aucton import Auction
import threading

# Начальное значение id
initial_id = 9800462


# Функция для выполнения запроса
def fetch_auction_data(start_id: int):
    id = start_id
    while True:
        print(f"Thread {threading.current_thread().name} is fetching id {id}")
        url = f"https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"

        try:
            resp = request(HTTPMethod.GET, url=url, timeout=3)
            if resp.ok:
                json_data = resp.json()
                try:
                    auction = Auction.model_validate(json_data)
                    # Здесь можно обработать объект auction, например, сохранить его
                    if len(auction.licenseFiles) > 0 or auction.isLicenseProduction or auction.uploadLicenseDocumentsComment is not None:
                        print(auction.id)
                    print(f"Auction {auction.id} fetched successfully in {threading.current_thread().name}")
                except ValueError as e:
                    print(f"Validation error for id {id} in {threading.current_thread().name}: {e}")
            else:
                print(f"Failed to fetch id {id} with status {resp.status_code}")
        except Exception as e:
            print(f"Request error for id {id}: {e}")

        id += 4  # Увеличиваем id с шагом 4 для параллельной обработки


# Создаем пул потоков и запускаем 4 задачи
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(fetch_auction_data, initial_id + i) for i in range(4)]

    # Опционально: можно ожидать завершения всех потоков, хотя в данном цикле они бесконечны
    for future in as_completed(futures):
        try:
            future.result()  # Получаем результат, если он есть (ожидаем завершения)
        except Exception as e:
            print(f"Thread raised an exception: {e}")
