#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pprint
import util
from website import (
    fetch_airchina,
    fetch_ceair,
    fetch_ch,
    fetch_csair,
    fetch_ctrip
)
from model.flight import Flight
from constant import (
    Website,
    CITY_NAME,
    EXEC_TIME,
)
from setting.subscribe_settings import (
    SUBSCRIBE_PERIODS,
    TOP_CHEAP_COUNT,
    PRICE_FLUCTUATION,
    IS_RECORD_HTML,
    IS_SEND_EMAIL,
)
import template.page


func_map = {
    Website.CTRIP: fetch_ctrip,
    Website.CEAIR: fetch_ceair,
    Website.CSAIR: fetch_csair,
    Website.CH: fetch_ch,
    Website.AIRCHINA: fetch_airchina,
}


def get_top_cheap_flights(period):
    last_fetch_time = Flight.get_last_fetch_time()
    if not last_fetch_time:
        return []
    params = {'from_city': period['from_city'], 'to_city': period['to_city'],
              'flight_date': period['date'], 'fetch_time': last_fetch_time}
    flights = Flight.select(**params)
    selected_flights = []
    for flight in flights:
        if flight['to_time'] < flight['from_time']:
            flight['to_time'] = str(int(flight['to_time'][0:2])+24) + \
                flight['to_time'][2:]
        if flight['from_airport'] in period['from_airport'] and \
                flight['to_airport'] in period['to_airport'] and \
                period['from_time'][0] <= flight['from_time'] \
                <= period['from_time'][1] and \
                period['to_time'][0] <= flight['to_time'] \
                <= period['to_time'][1]:
            selected_flights.append(flight)
    return sorted(selected_flights, key=lambda x: x['price'])[0:TOP_CHEAP_COUNT]


def get_price_trend(period):
    flights = Flight.select(from_city=period['from_city'],
                            to_city=period['to_city'],
                            flight_date=period['date'])
    result = {'all': _get_price_trend(flights)}
    for website in Website.ALL:
        result[website] = _get_price_trend(
            filter(lambda x: x['website'] == website, flights))
    return result


def _get_price_trend(flights):
    fetch_time_dict = {}
    for flight in flights:
        if flight['fetch_time'] in fetch_time_dict:
            fetch_time_dict[flight['fetch_time']].append(flight)
        else:
            fetch_time_dict[flight['fetch_time']] = [flight]
    result = []
    for fetch_time in sorted(fetch_time_dict.keys(), reverse=True):
        choose_flight = \
            sorted(fetch_time_dict[fetch_time], key=lambda x: x['price'])[0]
        if not result or \
                (result and abs(choose_flight['price']-result[-1]['price']) >
                    PRICE_FLUCTUATION):
            result.append(choose_flight)
    return result


def main():
    message_info = []
    trend_dict = {}
    for period in SUBSCRIBE_PERIODS:
        message_info.append({'from_city_name': CITY_NAME[period['from_city']],
                             'to_city_name': CITY_NAME[period['to_city']],
                             'from_city': period['from_city'],
                             'to_city': period['to_city'],
                             'date': period['date'],
                             'week_day_info': util.get_week_day(period['date']),
                             'flights': get_top_cheap_flights(period)})
        trend_dict[(period['date'], period['from_city'], period['to_city'])] =\
            get_price_trend(period)

    message_info = sorted(message_info, key=lambda x: x['date'])
    if message_info:
        tmp = template.page.get_html(message_info, trend_dict)
        if IS_RECORD_HTML:
            with open('html/%s.html' % EXEC_TIME.replace(' ', '_'), 'w') \
                    as handler:
                handler.write(tmp)
        if IS_SEND_EMAIL:
            util.send_email(tmp)

if __name__ == '__main__':
    main()