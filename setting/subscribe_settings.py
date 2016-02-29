#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from constant import Airport, City, CITY_TO_AIRPORTS
from setting import get_periods


TOP_CHEAP_COUNT = 6
PRICE_FLUCTUATION = 0
SUBSCRIBE_EMAIL = 'iwritepython@163.com'
IS_SEND_EMAIL = False
IS_RECORD_HTML = True

SUBSCRIBE_WEEK_NUM = 6
SUBSCRIBE_PERIODS = [
    {
        'from_time': ['16:00', '21:00'],
        'to_time': ['16:00', '23:59'],
        'to_airport': [Airport.HONGQIAO],
        'to_city': City.SHANGHAI,
        'from_city': City.CHONGQING,
        'week_day': 0,
    },
    {
        'from_time': ['18:00', '21:00'],
        'to_time': ['18:00', '22:40'],
        'from_airport': [Airport.HONGQIAO],
        'from_city': City.SHANGHAI,
        'to_city': City.CHONGQING,
        'week_day': 5,
    },
    {
        'from_time': ['06:00', '10:00'],
        'to_time': ['06:00', '13:00'],
        'from_airport': [Airport.HONGQIAO],
        'from_city': City.SHANGHAI,
        'to_city': City.CHONGQING,
        'week_day': 6,
    },
]
SUBSCRIBE_PERIODS = get_periods(SUBSCRIBE_PERIODS, SUBSCRIBE_WEEK_NUM)
# complete periods
for index, _period in enumerate(SUBSCRIBE_PERIODS):
    if not _period.get('from_airport'):
        SUBSCRIBE_PERIODS[index]['from_airport'] = \
            CITY_TO_AIRPORTS[_period['from_city']]
    if not _period.get('to_airport'):
        SUBSCRIBE_PERIODS[index]['to_airport'] = \
            CITY_TO_AIRPORTS[_period['to_city']]
    if not _period.get('from_time'):
        SUBSCRIBE_PERIODS[index]['from_time'] = ['00:00', '24:00']
    if not _period.get('to_time'):
        SUBSCRIBE_PERIODS[index]['to_time'] = ['00:00', '24:00']
# check settings
for _period in SUBSCRIBE_PERIODS:
    datetime.datetime.strptime(_period['date'], '%Y-%m-%d')
    if '00:00' <= _period['from_time'][0] <= '23:59' and \
            '00:00' <= _period['from_time'][1] <= '23:59' and \
            '00:00' <= _period['to_time'][1] <= '23:59' and \
            '00:00' <= _period['to_time'][1] <= '23:59':
        pass
    else:
        print 'error period', _period
        raise Exception

