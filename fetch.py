#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import util
import random
import traceback
from website import (
    fetch_airchina,
    fetch_ceair,
    fetch_ch,
    fetch_csair,
    fetch_ctrip
)
from tomorrow import threads

from settings import Website, AVAILABLE_WEBSITES, THREAD_COUNT, WEBSITE_NAME
from setting.fetch_settings import FETCH_PERIODS


func_map = {
    Website.CTRIP: fetch_ctrip,
    Website.CEAIR: fetch_ceair,
    Website.CSAIR: fetch_csair,
    Website.CH: fetch_ch,
    Website.AIRCHINA: fetch_airchina,
}
tasks = [(func_map[w], p, w) for p in FETCH_PERIODS for w in AVAILABLE_WEBSITES]
random.shuffle(tasks)


@threads(THREAD_COUNT)
def worker(task):
    module, period, website = task
    util.log_info('deal at %s %s %s' % (str(module), str(period), str(website)))
    try:
        module.fetch(period)
    except Exception as e:
        util.log_error(WEBSITE_NAME[website] + ' ' + str(e) + ' ' +
                       str(period) +
                       traceback.format_exc().replace('\n', '  |  '))


def fetch():
    for x in tasks:
        worker(x)

if __name__ == '__main__':
    fetch()
