"""
Тестирование функций клиента для получения информации о новостях.
"""

import pytest

from clients.news import NewsClient
from settings import API_KEY_NEWSAPI

@pytest.mark.asyncio
class TestClientNews:
    """
    Тестирование клиента для получения информации о новостях.
    """

    base_url = "https://newsapi.org/v2"

    @pytest.fixture
    def client(self):
        return  NewsClient()

    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    async def test_get_news(self, mocker, client):
        mocker.patch("clients.news.NewsClient._request")
        await client.get_news(country="AX")
        client._request.assert_called_once_with(f"{self.base_url}/top-headlines?country=AX&category=business&apiKey={API_KEY_NEWSAPI}")

        await client.get_news("test", "test")
        client._request.assert_called_with(f"{self.base_url}/top-headlines?country=test&category=test&apiKey={API_KEY_NEWSAPI}")