#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date

from django.shortcuts import render
from django.http import HttpResponseRedirect

from reports.functions import orders_statictic
from reports.functions.utils import get_date_from_str


def index(request):
    """Стартовая страница ввода дат"""
    return render(request, 'reports/index.html', locals())


def get_report(request):
    """Отчет"""
    if request.method == 'POST':
        begin_date = get_date_from_str(request.POST.get('begin_date')) if request.POST.get('begin_date') else \
            datetime.combine(datetime.now().date(), datetime.min.time())
        end_date = get_date_from_str(request.POST.get('end_date')) if request.POST.get('end_date') else \
            datetime.combine(datetime.now().date(), datetime.max.time())

        statistic = orders_statictic.get_orders_statistic(begin_date, end_date)

        return render(request, 'reports/orders_statistic.html', locals())

    return HttpResponseRedirect("/")
