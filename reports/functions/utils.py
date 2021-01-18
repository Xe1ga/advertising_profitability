#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date
from typing import Any

from django.db.models.query import QuerySet


def get_str_from_date(value: date) -> str:
    """
    Преобразует дату в строку
    :param value:
    :return:
    """
    return value.strftime('%d.%m.%Y')


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
