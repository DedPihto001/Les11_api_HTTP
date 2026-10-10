# Урок 11: HTTP-запросы и JSON

CLI-приложение отправляет GET-запросы, показывает полученный JSON и извлекает
название, столицу и регион из ответа World Bank API. Дополнительно в меню есть
запрос случайного изображения собаки.

## Установка и запуск

В PowerShell из папки `Les11` выполните:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Меню:

- `1` — выполнить GET-запрос по URL и вывести JSON;
- `2` — найти страну (название на английском или ISO-код) и вывести её
  название, столицу и регион;
- `3` — запросить случайное изображение собаки и вывести ссылку;
- `0` — выйти.

Приложение использует общий HTTP-модуль `http_client.py`: функция `get(url,
params=None, timeout=10)` выполняет запрос, проверяет HTTP-статус и возвращает
ответ в формате JSON.

## Примеры запросов вручную

Откройте ссылку ниже в браузере, чтобы увидеть JSON с полями страны:

```text
https://api.worldbank.org/v2/country/CA?format=json
```

Либо отправьте запрос из PowerShell:

```powershell
Invoke-RestMethod "https://api.worldbank.org/v2/country/CA?format=json" | ConvertTo-Json -Depth 5
```

Другой пример — JSON с URL случайного изображения собаки:

```text
https://dog.ceo/api/breeds/image/random
```

Для поиска по названию пункт `2` загружает список стран через World Bank API
и находит совпадение по английскому названию, ISO alpha-2 или alpha-3 коду.
Примеры выше можно проверить вручную, а затем выполнить запросы к этим API
через пункты `1`, `2` и `3` CLI-меню.

## Тесты

Тесты используют mock-ответы и не требуют подключения к внешним API:

```powershell
python -m unittest discover -s tests -v
```
