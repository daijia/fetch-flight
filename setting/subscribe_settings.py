#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
from constant import Airport, City

SUBSCRIBE_WEEK_NUM = 10
MAX_EMAIL_FLIGHT_COUNT = 8
PRICE_FLUCTUATION = 0


SUBSCRIBE_PERIODS = [
    {
        'begin_time': ['06:00', '23:00'],
        'end_time': ['06:00', '23:59'],
        'from_airport': [Airport.HONGQIAO, Airport.PUDONG],
        'to_airport': [Airport.JIANGBEI],
        'from_city': City.SHANGHAI,
        'to_city': City.CHONGQING,
        'date': '2016-03-01',
    },

    # {
    #     'begin_time': ['16:00', '21:00'],
    #     'end_time': ['16:00', '23:00'],
    #     'to_airport': [Airport.HONGQIAO, Airport.PUDONG],
    #     'from_airport': [Airport.JIANGBEI],
    #     'to_city': City.SHANGHAI,
    #     'from_city': City.CHONGQING,
    #     'week_day': 0,
    # },
    # {
    #     'begin_time': ['18:00', '21:00'],
    #     # 'end_time': ['14:00', '23:00'],
    #     'from_airport': [Airport.HONGQIAO],
    #     'to_airport': [Airport.JIANGBEI],
    #     'from_city': City.SHANGHAI,
    #     'to_city': City.CHONGQING,
    #     'week_day': 5,
    # },
    # {
    #     'begin_time': ['06:00', '10:00'],
    #     # 'end_time': ['14:00', '23:00'],
    #     'from_airport': [Airport.HONGQIAO],
    #     'to_airport': [Airport.JIANGBEI],
    #     'from_city': City.SHANGHAI,
    #     'to_city': City.CHONGQING,
    #     'week_day': 6,
    # },
]


def _get_dates(weekday):
    now_weekday = int(time.strftime("%w", time.localtime()))
    start_day = weekday - now_weekday
    if start_day < 0:
        start_day += 7
    days = range(start_day, start_day+SUBSCRIBE_WEEK_NUM*7, 7)
    dates = \
        [time.strftime('%Y-%m-%d', time.localtime(int(time.time())+3600*24*day))
         for day in days]
    return dates


_tmp_periods = list()
for _period in SUBSCRIBE_PERIODS:
    if _period.get('date'):
        _tmp_periods.append(_period)
    else:
        dates = _get_dates(_period['week_day'])
        for date in dates:
            _tmp_periods.append(_period.copy())
            _tmp_periods[-1].pop('week_day')
            _tmp_periods[-1]['date'] = date
SUBSCRIBE_PERIODS = _tmp_periods


# check settings
for _period in SUBSCRIBE_PERIODS:
    datetime.datetime.strptime(_period['date'], '%Y-%m-%d')
    if '00:00' <= _period['begin_time'][0] <= '23:59' and \
            '00:00' <= _period['begin_time'][1] <= '23:59' and \
            '00:00' <= _period['end_time'][1] <= '23:59' and \
            '00:00' <= _period['end_time'][1] <= '23:59':
        pass
    else:
        print 'error period', _period
        raise Exception

