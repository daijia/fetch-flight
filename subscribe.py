#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import util
import random
from website import (
    fetch_airchina,
    fetch_ceair,
    fetch_ch,
    fetch_csair,
    fetch_ctrip
)
from tomorrow import threads

from model.flight import Flight
from constant import *
from setting.subscribe_settings import *
import template.page


func_map = {
    Website.CTRIP: fetch_ctrip,
    Website.CEAIR: fetch_ceair,
    Website.CSAIR: fetch_csair,
    Website.CH: fetch_ch,
    Website.AIRCHINA: fetch_airchina,
}
msg_dict = dict()
tasks = [(func_map[w], p, w) for p in PERIODS for w in AVAILABLE_WEBSITES]
random.shuffle(tasks)
exec_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())


@threads(THREAD_COUNT)
def worker(task):
    module, period, website = task
    print module, period, website
    try:
        result = module.fetch(period)
    except Exception as e:
        print 'error', str(e), period, WEBSITE_NAME[website]
        result = []
    return period, result


def fetch():
    results = [worker(x) for x in tasks]
    for x in results:
        period, result = x
        if str(period) in msg_dict:
            msg_dict[str(period)] += result
        else:
            msg_dict[str(period)] = result


def format_data():
    message_info = []
    trend_dict = {}
    for period in PERIODS:
        message_info.append({'from_city_name': CITY_NAME[period['from_city']],
                             'to_city_name': CITY_NAME[period['to_city']],
                             'from_city': period['from_city'],
                             'to_city': period['to_city'],
                             'date': period['date'],
                             'week_day_info': util.get_week_day(period['date']),
                             'lines': sorted(msg_dict.get(str(period), []),
                                             key=lambda x: x[-1][-1])
                             [0:MAX_EMAIL_FLIGHT_COUNT]})
        for line in message_info[-1]['lines']:
            _date, website, url, flight = line
            Flight.insert(from_airport=flight[1],
                          to_airport=flight[4],
                          from_time=flight[2],
                          to_time=flight[5],
                          from_city=period['from_city'],
                          to_city=period['to_city'],
                          website=website,
                          price=flight[-1],
                          flight_date=period['date'],
                          detail=flight[0][0:20],
                          url=url,
                          fetch_time=exec_time.replace('_', ' '),
                          time_range='(%s %s) (%s %s)' % (
                              period['begin_time'][0],
                              period['begin_time'][1],
                              period['end_time'][0],
                              period['end_time'][1]))
        trend_dict[(period['date'], period['from_city'], period['to_city'])] =\
            util.get_price_trend(period)

    # print pprint.pprint(trend_dict)
    message_info = sorted(message_info, key=lambda x: x['date'])
    if message_info:
        tmp = template.page.get_html(message_info, trend_dict)
        with open('html/%s.html' % exec_time, 'w') \
                as handler:
            handler.write(tmp)

if __name__ == '__main__':
    fetch()
    format_data()