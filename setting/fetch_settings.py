#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
from settings import City, Website, Airport

FETCH_WEEK_NUM = 1

FETCH_PERIODS = [
    # {
    #     'from_city': City.SHANGHAI,
    #     'to_city': City.CHONGQING,
    #     'date': '2016-03-03',
    # },
    {
        'to_city': City.SHANGHAI,
        'from_city': City.CHONGQING,
        'week_day': 0,
    },
    # {
    #     'from_city': City.SHANGHAI,
    #     'to_city': City.CHONGQING,
    #     'week_day': 5,
    # },
    # {
    #     'from_city': City.SHANGHAI,
    #     'to_city': City.CHONGQING,
    #     'week_day': 6,
    # },
]


AIRPORT_NAME_PARAMS = {
    Website.CTRIP: {Airport.HONGQIAO: u'虹桥国际机场', Airport.PUDONG: u'浦东国际机场',
                    Airport.JIANGBEI: u'江北国际机场'},
    Website.CEAIR: {Airport.HONGQIAO: u'虹桥机场', Airport.PUDONG: u'浦东机场',
                    Airport.JIANGBEI: u'江北机场'},
    Website.CSAIR: {Airport.HONGQIAO: u'上海虹桥', Airport.PUDONG: u'上海浦东',
                    Airport.JIANGBEI: u'重庆'},
    Website.CH: {Airport.HONGQIAO: u'上海虹桥', Airport.PUDONG: u'上海浦东',
                 Airport.JIANGBEI: u'重庆江北'},
    Website.AIRCHINA: {Airport.HONGQIAO: u'SHA',
                       Airport.PUDONG: u'PVG',
                       Airport.JIANGBEI: u'CKG'},
}


URL_PARAMS = {
    Website.CTRIP: {City.SHANGHAI: u'SHA', City.CHONGQING: u'CKG'},
    Website.CEAIR: {City.SHANGHAI: u'pvg', City.CHONGQING: u'ckg'},
    Website.CSAIR: {Airport.HONGQIAO: u'SHA', Airport.JIANGBEI: u'CKG',
                    Airport.PUDONG: u'PVG'},
    Website.CH: {City.SHANGHAI: (u'上海', u'SHA'),
                 City.CHONGQING: (u'重庆', u'CKG')},
    Website.AIRCHINA: {Airport.HONGQIAO: u'SHA',
                       Airport.JIANGBEI: u'CKG',
                       Airport.PUDONG: u'PVG'},
}


def _get_dates(weekday):
    now_weekday = int(time.strftime("%w", time.localtime()))
    start_day = weekday - now_weekday
    if start_day < 0:
        start_day += 7
    days = range(start_day, start_day+FETCH_WEEK_NUM*7, 7)
    dates = \
        [time.strftime('%Y-%m-%d', time.localtime(int(time.time())+3600*24*day))
         for day in days]
    return dates


_tmp_periods = list()
for _period in FETCH_PERIODS:
    if _period.get('date'):
        _tmp_periods.append(_period)
    else:
        dates = _get_dates(_period['week_day'])
        for date in dates:
            _tmp_periods.append(_period.copy())
            _tmp_periods[-1].pop('week_day')
            _tmp_periods[-1]['date'] = date
FETCH_PERIODS = _tmp_periods


# check settings
for _period in FETCH_PERIODS:
    datetime.datetime.strptime(_period['date'], '%Y-%m-%d')
