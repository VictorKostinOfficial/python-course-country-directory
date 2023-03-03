"""
Функции для формирования выходной информации.
"""
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> tuple[list, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """
        result = (
            ["Location Info",       "-------------------------------"],
            ["Страна",              f"{self.location_info.location.name}"],
            ["Столица",             f"{self.location_info.location.capital}"],
            ["Регион",              f"{self.location_info.location.subregion}"],
            ["Часовой пояс",        f"{self.location_info.location.timezones[0]}"],
            ["Время",               f"{await self._format_timezone()}"],
            ["Широта",              f"{self.location_info.location.latitude}°"],
            ["Долгота",             f"{self.location_info.location.longitude}°"],
            ["Языки",               f"{await self._format_languages()}"],
            ["Население страны",    f"{await self._format_population()} чел."],
            ["Площадь страны",      f"{self.location_info.location.area} чел."],
            ["Weather Info",        "-------------------------------"],
            ["Погода",              f"{self.location_info.weather.temp} °C"],
            ["Описание погоды",     f"{self.location_info.weather.description}"],
            ["Давление",            f"{self.location_info.weather.pressure} мм рт. ст."],
            ["Влажность",           f"{self.location_info.weather.humidity}%"],
            ["Скорость ветра",      f"{self.location_info.weather.wind_speed} м\с"],
            ["Видимость",           f"{self.location_info.weather.visibility} м"],
            ["Currency Info",       "-------------------------------"],
            ["Курсы валют",         f"{await self._format_currency_rates()}"],
            ["News Info",           "-------------------------------"],
        )

        length = len(self.location_info.news.articles)
        if length > 5: length = 5
        for index in range(length):
            result = (*result, [f"{self.location_info.news.articles.pop().author}",
                                  f"{self.location_info.news.articles.pop().title}"],)

        return result

    async def _format_timezone(self) -> str:
        """
        Форматирование информации о времени.

        :return:
        """
        hours = float(self.location_info.location.timezones[0][3:6])
        minutes = float(self.location_info.location.timezones[0][3:4] + self.location_info.location.timezones[0][7:9])
        return (datetime.utcnow() + timedelta(hours= hours, minutes=minutes)).__format__("%H:%M:%S")

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
