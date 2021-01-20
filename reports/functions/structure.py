#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NamedTuple


class OrdersStatistic(NamedTuple):
    """Структура для отчета orders_statistic"""
    date: str
    clicks: str
    orders_in_processing: str
    orders_approved: str
    orders_canceled: str
    orders_affiliate_fee: str


class DBData(NamedTuple):
    """Структура для отчета orders_statistic"""
    clicks_statistic: dict
    ordered_for_status_in_processed: dict
    ordered_for_status_approved: dict
    ordered_for_status_canceled: dict
    orders_affiliate_fee: dict


