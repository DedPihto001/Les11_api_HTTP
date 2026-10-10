"""Simple Russian-language CLI for practicing JSON API requests."""

import json
from typing import Any

import requests

from country_info import get_country_info
from http_client import get


DOG_API_URL = "https://dog.ceo/api/breeds/image/random"


def get_random_dog_image() -> str:
    """Return the image URL from the random dog API."""
    payload: Any = get(DOG_API_URL)
    if not isinstance(payload, dict) or not isinstance(payload.get("message"), str):
        raise ValueError("API вернул неожиданный формат данных о собаке.")
    return payload["message"]


def print_json(payload: Any) -> None:
    """Print a Python JSON value in a readable format."""
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def run_menu() -> None:
    while True:
        print(
            "\nМеню:\n"
            "1 — GET по URL\n"
            "2 — Информация о стране\n"
            "3 — Случайная собака\n"
            "0 — Выход"
        )
        choice = input("Выберите пункт: ").strip()

        if choice == "0":
            print("До свидания!")
            return

        try:
            if choice == "1":
                url = input("Введите URL: ").strip()
                if not url:
                    raise ValueError("URL не должен быть пустым.")
                print_json(get(url))
            elif choice == "2":
                country_name = input(
                    "Введите название страны на английском или ISO-код: "
                )
                print_json(get_country_info(country_name))
            elif choice == "3":
                print(f"Ссылка на изображение: {get_random_dog_image()}")
            else:
                print("Неизвестный пункт меню. Выберите 1, 2, 3 или 0.")
        except requests.RequestException as error:
            print(f"Ошибка HTTP-запроса: {error}")
        except ValueError as error:
            print(f"Ошибка данных: {error}")


if __name__ == "__main__":
    run_menu()
