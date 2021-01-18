#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date

from django.shortcuts import render

from reports.functions import orders_statictic


def index(request):
    """Стартовая страница приложения reports"""
    begin_date = datetime.combine(date(2016, 9, 10), datetime.min.time())
    end_date = datetime.combine(date(2016, 9, 13), datetime.max.time())

    statistic = orders_statictic.get_orders_statistic(begin_date, end_date)

    return render(request, 'reports/orders_statistic.html', locals())
