#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from typing import Any, Optional, Generator


def get_str_from_date(value: date) -> str:
    """
    Преобразует дату в строку
    :param value:
    :return:
    """
    return value.strftime('%d.%m.%Y')


def get_date_with_min_time(value: str) -> date:
    """
    Преобразует дату в строку
    :param value:
    :return:
    """
    return datetime.combine(datetime.strptime(value, "%d.%m.%Y"), datetime.min.time())


def get_date_with_max_time(value: str) -> date:
    """
    Преобразует дату в строку
    :param value:
    :return:
    """
    return datetime.combine(datetime.strptime(value, "%d.%m.%Y"), datetime.max.time())


def get_dict(function_to_decorate):
    """
    Получить новый словарь, ключи  - даты, значения -  показатели критерия
    :param function_to_decorate:
    :return:
    """

    def wrap(*args: Any, **kwargs: Any) -> dict:
        """
        Обертка словарь
        :param args:
        :param kwargs:
        :return:
        """
        data = function_to_decorate(*args, **kwargs)
        result = {}
        for rec in data:
            key = get_str_from_date(rec["date"])
            val = str(rec["metric"]) if rec["metric"] else 0
            result[key] = val
        return result

    return wrap


def exclude_none(value: Optional[str]) -> str:
    """
    Возвращает строку с 0 вместо None, если Values None
    :param value:
    :return:
    """
    return value if value else "0"


def date_generator(begin_date: datetime, end_date: datetime) -> Generator:
    """
    Генератор дат
    :param begin_date:
    :param end_date:
    :return:
    """
    while begin_date <= end_date:
        yield get_str_from_date(begin_date.date())
        begin_date = begin_date + timedelta(days=1)
