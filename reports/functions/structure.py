#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NamedTuple


class OrdersStatistic(NamedTuple):
    """Структура для отчета orders_statistic"""
    data: str
    clicks: str
    orders_in_processed: str
    orders_approved: str
    orders_canceled: str
    orders_affiliate_fee: str
