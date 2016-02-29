#!/usr/bin/env python
# -*- coding: utf-8 -*-
import util
from selenium import webdriver
from settings import Website, CITY_TO_AIRPORTS, AIRLINE_NAME
from setting.fetch_settings import AIRPORT_NAME_PARAMS, URL_PARAMS


def dig_info(flight, pair):
    try:
        elements = [x.strip() for x in flight.text.split('\n')]
        flight_no, from_time, from_airport, to_time, to_airport, prices = \
            '', None, None, None, None, []
        flight_no = flight.find_element_by_class_name('sp-trip-stops').text.\
            strip()
        for element in elements:
            if len(element) >= 5 and '00:00' <= element[0:5] <= '23:59':
                if not from_time:
                    from_time = element[0:5]
                else:
                    to_time = element[0:5]
            if element == AIRPORT_NAME_PARAMS[Website.CSAIR][pair[0]]:
                from_airport = element
            if element == AIRPORT_NAME_PARAMS[Website.CSAIR][pair[1]]:
                to_airport = element
            if element.startswith(u'¥ '):
                price = element[2:].replace(',', '').strip()
                digits = []
                for digit in price:
                    if digit.isdigit():
                        digits.append(digit)
                    else:
                        break
                if not digits:
                    continue
                prices.append(int(''.join(digits)))
        if not (from_time and from_airport and to_time and
                to_airport and prices):
            util.log_error(u'CSAIR: 抓取内容失败')
            return None
        from_time_pair = [int(x) for x in from_time.split(':')]
        to_time_pair = [int(x) for x in to_time.split(':')]
        if to_time_pair[0] < from_time_pair[0]:
            to_time_pair[0] += 24
        price = min(prices)
        return [AIRLINE_NAME[Website.CSAIR], flight_no, from_airport, from_time,
                from_time_pair, to_airport, to_time, to_time_pair, price]
    except Exception as e:
        util.log_error('CSAIR: ' + str(e))
        return None


def fetch(period):
    format_flights = []
    airport_pairs = [(x, y) for x in CITY_TO_AIRPORTS[period['from_city']]
                     for y in CITY_TO_AIRPORTS[period['to_city']]]
    url = ''
    for pair in airport_pairs:
        browser = webdriver.PhantomJS()
        url = 'http://b2c.csair.com/B2C40/modules/bookingnew/main/' \
              'flightSelectDirect.html?t=S&c1=%s&c2=%s&d1=%s&at=1&ct=0&it=0' % \
              (URL_PARAMS[Website.CSAIR][pair[0]],
               URL_PARAMS[Website.CSAIR][pair[1]],
               period['date'])
        browser.get(url)
        block = util.fetch_one(browser, 'find_element_by_class_name',
                               'sp-trip-body')
        if not block:
            continue
        flights = util.fetch_multi(block, 'find_elements_by_tag_name', 'ul')
        for flight in flights:
            info = dig_info(flight, pair)
            if info:
                format_flights.append(info)
        browser.quit()
    return util.deal(period, format_flights, Website.CSAIR, url)

