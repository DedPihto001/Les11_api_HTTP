"""Country lookup using the World Bank API."""

from typing import Any

from http_client import get


COUNTRY_API_URL = "https://api.worldbank.org/v2/country"


def get_country_info(country_name: str) -> dict[str, str | int]:
    """Return a few useful fields for the first country matching the name."""
    country_name = country_name.strip()
    if not country_name:
        raise ValueError("Введите название страны.")

    payload: Any = get(COUNTRY_API_URL, params={"format": "json", "per_page": "1000"})
    if (
        not isinstance(payload, list)
        or len(payload) < 2
        or not isinstance(payload[1], list)
    ):
        raise ValueError("API вернул неожиданный формат данных о стране.")

    lookup_name = country_name.casefold()
    country = next(
        (
            item
            for item in payload[1]
            if isinstance(item, dict)
            and lookup_name
            in {
                value.casefold()
                for value in (item.get("name"), item.get("id"), item.get("iso2Code"))
                if isinstance(value, str)
            }
        ),
        None,
    )
    if country is None:
        raise ValueError(
            "Страна не найдена. Введите название на английском или код ISO."
        )

    name = country.get("name")
    capital = country.get("capitalCity")
    region_data = country.get("region")
    if (
        not isinstance(name, str)
        or not isinstance(capital, str)
        or not isinstance(region_data, dict)
        or not isinstance(region_data.get("value"), str)
    ):
        raise ValueError("В ответе API отсутствуют поля страны.")

    return {
        "Страна": name,
        "Столица": capital or "Не указана",
        "Регион": region_data["value"].strip(),
    }
