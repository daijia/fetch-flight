#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


def _get_dates(weekday, week_num):
    now_weekday = int(time.strftime("%w", time.localtime()))
    start_day = weekday - now_weekday
    if start_day < 0:
        start_day += 7
    days = range(start_day, start_day+week_num*7, 7)
    dates = \
        [time.strftime('%Y-%m-%d', time.localtime(int(time.time())+3600*24*day))
         for day in days]
    return dates


def get_periods(origin_periods, week_num):
    _tmp_periods = list()
    for _period in origin_periods:
        if _period.get('date'):
            _tmp_periods.append(_period)
        else:
            dates = _get_dates(_period['week_day'], week_num)
            for date in dates:
                _tmp_periods.append(_period.copy())
                _tmp_periods[-1].pop('week_day')
                _tmp_periods[-1]['date'] = date
    return _tmp_periods
