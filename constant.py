#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


class City(object):
    SHANGHAI = 1
    CHONGQING = 3
    ALL = [SHANGHAI, CHONGQING]


class Airport(object):
    HONGQIAO = 1
    PUDONG = 2
    JIANGBEI = 3
    ALL = [HONGQIAO, PUDONG, JIANGBEI]


class Website(object):
    CTRIP = 1
    CEAIR = 2
    AIRCHINA = 3
    CH = 4
    CSAIR = 5
    ALL = [CTRIP, CH, CEAIR, CSAIR, AIRCHINA]


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


AIRLINE_NAME = {
    Website.CEAIR: u'东方航空',
    Website.AIRCHINA: u'中国国航',
    Website.CH: u'春秋航空',
    Website.CSAIR: u'南方航空',
}


AIRPORT_NAME = {
    Airport.HONGQIAO: u'上海虹桥',
    Airport.PUDONG: u'上海浦东',
    Airport.JIANGBEI: u'重庆江北',
}

CITY_TO_AIRPORTS = {
    City.SHANGHAI: [Airport.HONGQIAO, Airport.PUDONG],
    City.CHONGQING: [Airport.JIANGBEI],
}

AIRPORT_TO_CITY = {
    Airport.HONGQIAO: City.SHANGHAI,
    Airport.PUDONG: City.SHANGHAI,
    Airport.JIANGBEI: City.CHONGQING,
}


EXEC_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


