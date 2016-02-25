#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from website import fetch_airchina, fetch_ceair, fetch_ch, fetch_csair, \
    fetch_ctrip
from settings import *
import util
import random
import template.page
reload(sys)
sys.setdefaultencoding('utf8')
from tomorrow import threads


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


@threads(5)
def worker(task):
    module, period, website = task
    try:
        result = module.fetch(period)
    except Exception as e:
        print 'error', str(e), period, WEBSITE_NAME[website]
        result = []
    return period, result


def fetch():
    message_info = []
    for period in PERIODS:
        message_info.append({'from_city': CITY_NAME[period['from_city']],
                             'to_city': CITY_NAME[period['to_city']],
                             'date': period['date'],
                             'week_day_info': util.get_week_day(period['date']),
                             'lines': sorted(msg_dict.get(str(period), []),
                                             key=lambda x: x[-1][-1])})
    message_info = sorted(message_info, key=lambda x: x['date'])
    if message_info:
        tmp = template.page.get_html(message_info)
        with open('html/%s.html' %
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'w') \
                as handler:
            handler.write(tmp)

results = [worker(x) for x in tasks]
for x in results:
    period, result = x
    if str(period) in msg_dict:
        msg_dict[str(period)] += result
    else:
        msg_dict[str(period)] = result

fetch()