import unittest
from unittest.mock import Mock, patch

import http_client
from country_info import get_country_info
from main import get_random_dog_image


class HttpClientTests(unittest.TestCase):
    @patch("http_client.requests.get")
    def test_get_checks_status_and_returns_json(self, request_get: Mock) -> None:
        response = request_get.return_value
        response.json.return_value = {"ok": True}

        result = http_client.get("https://example.test/data", {"q": "value"})

        request_get.assert_called_once_with(
            "https://example.test/data",
            params={"q": "value"},
            timeout=10,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, {"ok": True})

    @patch("http_client.requests.get")
    def test_get_propagates_http_errors(self, request_get: Mock) -> None:
        response = request_get.return_value
        response.raise_for_status.side_effect = http_client.requests.HTTPError("404")

        with self.assertRaises(http_client.requests.HTTPError):
            http_client.get("https://example.test/missing")

        response.json.assert_not_called()


class ApiParsingTests(unittest.TestCase):
    @patch("country_info.get")
    def test_country_info_extracts_key_fields(self, api_get: Mock) -> None:
        api_get.return_value = [
            {"page": 1, "pages": 1, "total": 1},
            [
                {
                    "id": "CAN",
                    "iso2Code": "CA",
                    "name": "Canada",
                    "capitalCity": "Ottawa",
                    "region": {
                        "id": "NAC",
                        "iso2code": "XU",
                        "value": "North America",
                    },
                }
            ],
        ]

        result = get_country_info(" Canada ")

        self.assertEqual(
            result,
            {
                "Страна": "Canada",
                "Столица": "Ottawa",
                "Регион": "North America",
            },
        )
        api_get.assert_called_once_with(
            "https://api.worldbank.org/v2/country",
            params={"format": "json", "per_page": "1000"},
        )

    @patch("main.get")
    def test_random_dog_returns_image_url(self, api_get: Mock) -> None:
        api_get.return_value = {
            "message": "https://images.dog.ceo/breeds/example.jpg",
            "status": "success",
        }

        self.assertEqual(
            get_random_dog_image(),
            "https://images.dog.ceo/breeds/example.jpg",
        )

    def test_country_info_rejects_empty_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "название страны"):
            get_country_info("  ")


if __name__ == "__main__":
    unittest.main()
