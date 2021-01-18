#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.db.models.query import QuerySet

from reports.models import Orders, Statistic


def get_orders_in_processing(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество заказов в обработке в разбивке по дням, status = 0
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_in_processing = Orders.objects.filter(created_at__gte=begin_date, created_at__lte=end_date, status=0)

    return orders_in_processing


def get_orders_approved(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням, status >= 10
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_approved = Orders.objects.filter(created_at__gte=begin_date, created_at__lte=end_date, status__gte=10)

    return orders_approved


def get_orders_canceled(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням, status >= 10
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_canceled = Orders.objects.filter(created_at__gte=begin_date, created_at__lte=end_date, status__lt=0)

    return orders_canceled


def get_orders_affiliate_fee(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням, status >= 10
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_affiliate_fee = Orders.objects.filter(created_at__gte=begin_date, created_at__lte=end_date).\
        annotate(date=TruncDate('created_at')).\
        values('date').\
        annotate(in_processing=Sum('affiliate_fee')).\
        order_by('date')
    print(orders_affiliate_fee)
    return orders_affiliate_fee


def get_ordered_for_status(begin_date: date, end_date: date, filter_by_status: str) -> QuerySet:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням в зависимости от статуса
    :param begin_date:
    :param end_date:
    :param filter_by_status:
    :return:
    """
    orders_filter = {
        'in processing': get_orders_in_processing(begin_date, end_date),
        'approved': get_orders_approved(begin_date, end_date),
        'canceled': get_orders_canceled(begin_date, end_date)
    }

    query_set = orders_filter[filter_by_status].\
        annotate(date=TruncDate('created_at')).\
        values('date').\
        annotate(in_processing=Count('status')).\
        order_by('date')

    return query_set


def get_clicks_statistic(begin_date: date, end_date: date) -> QuerySet:
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


def get_orders_statistic(begin_date: date, end_date: date):
    """
    Возвращает статистику доходности
    :param begin_date:
    :param end_date:
    :return:
    """
    # for click_stat in get_clicks_statistic(begin_date, end_date):

    return get_orders_affiliate_fee(begin_date, end_date), get_clicks_statistic(begin_date, end_date)
