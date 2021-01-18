#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

from reports.models import Orders, Statistic


def get_orders(begin_date: date, end_date: date) -> object:
    """
    Возвращает результат запроса к таблице Orders
    :param begin_date:
    :param end_date:
    :return:
    """
    orders = Orders.objects.\
        filter(created_at__gte=begin_date, created_at__lte=end_date, status=0).\
        annotate(date=TruncDate('created_at')). \
        values('date'). \
        annotate(in_processing=Count('status')). \
        order_by('date')
    print(orders)
    print(orders.query)
    return orders


def get_clicks_statistic(begin_date: date, end_date: date) -> object:
    """
    Возвращает результат запроса к таблице Statistic
    :param begin_date:
    :param end_date:
    :return:
    """
    statistic = Statistic.objects.values('date').\
        filter(date__gte=begin_date.date(), date__lte=end_date.date()).\
        annotate(clicks_uniq_sum=Sum('clicks_uniq')).\
        order_by('date')

    return statistic


def get_orders_statistic(begin_date: date, end_date: date) -> dict:
    """
    Возвращает статистику доходности
    :param begin_date:
    :param end_date:
    :return:
    """

    return get_orders(begin_date, end_date), get_clicks_statistic(begin_date, end_date)
