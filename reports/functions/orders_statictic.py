#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.db.models.query import QuerySet
from django.utils import timezone

from reports.models import Orders, Statistic
from reports.functions.structure import OrdersStatistic, DBData
from reports.functions.utils import get_dict, exclude_none, date_generator


def get_orders_in_processing(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество заказов в обработке в разбивке по дням, status = 0
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_in_processing = Orders.objects.filter(created_at__gte=timezone.make_aware(begin_date),
                                                 created_at__lte=timezone.make_aware(end_date), status=0)

    return orders_in_processing


def get_orders_approved(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням, status >= 10
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_approved = Orders.objects.filter(created_at__gte=timezone.make_aware(begin_date),
                                            created_at__lte=timezone.make_aware(end_date), status__gte=10)

    return orders_approved


def get_orders_canceled(begin_date: date, end_date: date) -> QuerySet:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням, status >= 10
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_canceled = Orders.objects.filter(created_at__gte=timezone.make_aware(begin_date),
                                            created_at__lte=timezone.make_aware(end_date), status__lt=0)

    return orders_canceled


@get_dict
def get_orders_affiliate_fee(begin_date: date, end_date: date) -> dict:
    """
    Возвращает количество подтвержденных заказов в разбивке по дням, status >= 10
    :param begin_date:
    :param end_date:
    :return:
    """
    orders_affiliate_fee = Orders.objects.filter(created_at__gte=timezone.make_aware(begin_date),
                                                 created_at__lte=timezone.make_aware(end_date)). \
        annotate(date=TruncDate('created_at')). \
        values('date'). \
        annotate(metric=Sum('affiliate_fee')). \
        order_by('date')

    return orders_affiliate_fee


@get_dict
def get_ordered_for_status(begin_date: date, end_date: date, filter_by_status: str) -> dict:
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

    query_set = orders_filter[filter_by_status]. \
        annotate(date=TruncDate('created_at')). \
        values('date'). \
        annotate(metric=Count('status')). \
        order_by('date')

    return query_set


@get_dict
def get_clicks_statistic(begin_date: datetime, end_date: datetime) -> dict:
    """
    Возвращает результат запроса к таблице Statistic
    :param begin_date:
    :param end_date:
    :return:
    """
    statistic = Statistic.objects.values('date'). \
        filter(date__gte=begin_date, date__lte=end_date). \
        annotate(metric=Sum('clicks_uniq')). \
        order_by('date')

    return statistic


def get_db_data(begin_date: datetime, end_date: datetime) -> DBData:
    """
    Запросить данные и сформировать струкруру для хранения данных из БД
    :param begin_date:
    :param end_date:
    :return:
    """
    db_data = DBData(
        clicks_statistic=get_clicks_statistic(begin_date, end_date),
        ordered_for_status_in_processed=get_ordered_for_status(begin_date, end_date, 'in processing'),
        ordered_for_status_approved=get_ordered_for_status(begin_date, end_date, 'approved'),
        ordered_for_status_canceled=get_ordered_for_status(begin_date, end_date, 'canceled'),
        orders_affiliate_fee=get_orders_affiliate_fee(begin_date, end_date)
    )
    return db_data


def get_orders_statistic(begin_date: datetime, end_date: datetime):
    """
    Возвращает статистику доходности
    :param begin_date:
    :param end_date:
    :return:
    """
    db_data = get_db_data(begin_date, end_date)
    statistic = (OrdersStatistic(date=created_date,
                                 clicks=exclude_none(db_data.clicks_statistic.get(created_date)),
                                 orders_in_processing=exclude_none(
                                     db_data.ordered_for_status_in_processed.get(created_date)),
                                 orders_approved=exclude_none(db_data.ordered_for_status_approved.get(created_date)),
                                 orders_canceled=exclude_none(db_data.ordered_for_status_canceled.get(created_date)),
                                 orders_affiliate_fee=exclude_none(db_data.orders_affiliate_fee.get(created_date))
                                 )
                 for created_date in date_generator(begin_date, end_date))

    result = filter(lambda stat: sum([float(stat.clicks),
                                      float(stat.orders_in_processing),
                                      float(stat.orders_approved),
                                      float(stat.orders_canceled),
                                      float(stat.orders_affiliate_fee)]),
                    statistic)

    return result
