#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime


class City(object):
    SHANGHAI = 0
    CHONGQING = 1


class Airport(object):
    HONGQIAO = 0
    PUDONG = 1
    JIANGBEI = 2


class Website(object):
    CTRIP = 0
    CEAIR = 3
    AIRCHINA = 4
    CH = 5
    CSAIR = 6


THREAD_COUNT = 5
AVAILABLE_WEBSITES = [Website.CTRIP, Website.CH, Website.CEAIR, Website.CSAIR,
                      Website.AIRCHINA]
WEEK_NUM = 10
MAX_EMAIL_FLIGHT_COUNT = 8
MAX_STORE_FLIGHT_COUNT = 20
PRICE_FLUCTUATION = 0


PERIODS = [
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

WEBSITE_NAME = {
    Website.CTRIP: u'携程',
    Website.CEAIR: u'东航',
    Website.AIRCHINA: u'国航',
    Website.CH: u'春秋',
    Website.CSAIR: u'南航',
}

CITY_NAME = {
    City.SHANGHAI: u'上海',
    City.CHONGQING: u'重庆',
}


AIRPORT_NAME = {
    Airport.HONGQIAO: u'上海虹桥',
    Airport.PUDONG: u'上海浦东',
    Airport.JIANGBEI: u'重庆江北'
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


def get_dates(weekday):
    now_weekday = int(time.strftime("%w", time.localtime()))
    start_day = weekday - now_weekday
    if start_day < 0:
        start_day += 7
    days = range(start_day, start_day+WEEK_NUM*7, 7)
    dates = \
        [time.strftime('%Y-%m-%d', time.localtime(int(time.time())+3600*24*day))
         for day in days]
    return dates


_tmp_periods = list()
for _period in PERIODS:
    if _period.get('date'):
        _tmp_periods.append(_period)
    else:
        dates = get_dates(_period['week_day'])
        for date in dates:
            _tmp_periods.append(_period.copy())
            _tmp_periods[-1].pop('week_day')
            _tmp_periods[-1]['date'] = date
PERIODS = _tmp_periods


# check settings
for _period in PERIODS:
    datetime.datetime.strptime(_period['date'], '%Y-%m-%d')
    if '00:00' <= _period['begin_time'][0] <= '23:59' and \
            '00:00' <= _period['begin_time'][1] <= '23:59' and \
            '00:00' <= _period['end_time'][1] <= '23:59' and \
            '00:00' <= _period['end_time'][1] <= '23:59':
        pass
    else:
        print 'error period', _period
        raise Exception

