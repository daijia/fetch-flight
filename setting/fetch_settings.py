#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from constant import City, Website, Airport
from setting import get_periods

FETCH_WEBSITES = Website.ALL
THREAD_COUNT = 5

FETCH_WEEK_NUM = 8
FETCH_PERIODS = [
    {
        'to_city': City.SHANGHAI,
        'from_city': City.CHONGQING,
        'week_day': 0,
    },
    {
        'from_city': City.SHANGHAI,
        'to_city': City.CHONGQING,
        'week_day': 5,
    },
    {
        'from_city': City.SHANGHAI,
        'to_city': City.CHONGQING,
        'week_day': 6,
    },
]
FETCH_PERIODS = get_periods(FETCH_PERIODS, FETCH_WEEK_NUM)
# check settings
for _period in FETCH_PERIODS:
    datetime.datetime.strptime(_period['date'], '%Y-%m-%d')


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


