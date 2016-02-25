#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import util
from selenium import webdriver


def dig_info(flight):
    try:
        part1 = flight.find_element_by_class_name('f-i').text
        elements = [x.strip() for x in part1.split('\n')]
        info = elements[0].replace('|', ' ').strip()
        tmp_elements = []
        for element in elements:
            if '00:00' <= element <= '23:59':
                tmp_elements.append(element[0:5])
            elif any([element.startswith(x) for x in AIRPORT_NAME_PARAMS[Website.CEAIR].values()]):
                tmp_elements.append(element)
        from_time, from_airport, to_time, to_airport = tmp_elements

        from_time_pair = [int(x) for x in from_time.split(':')]
        to_time_pair = [int(x) for x in to_time.split(':')]
        if to_time_pair[0] < from_time_pair[0]:
            to_time_pair[0] += 24

        elements = [x.strip() for x in flight.text.split('\n')]
        prices = []
        for element in elements:
            if element.startswith(u'￥'):
                price = element[1:].replace(',', '')
                digits = []
                for digit in price:
                    if digit.isdigit():
                        digits.append(digit)
                    else:
                        break
                if not digits:
                    continue
                prices.append(int(''.join(digits)))
        if not prices:
            return None
        price = min(prices)
        return [' '.join(info.split()), from_airport, from_time,
                from_time_pair, to_airport, to_time, to_time_pair, price]
    except Exception as e:
        return None


def fetch(period):
    browser = webdriver.PhantomJS()
    url = 'http://www.ceair.com/flight2014/%s-%s-%s_CNY.html' % \
        (URL_PARAMS[Website.CEAIR][period['from_city']],
         URL_PARAMS[Website.CEAIR][period['to_city']],
         period['date'][2:].replace('-', ''))
    browser.get(url)
    block = util.fetch_one(browser, 'find_element_by_id', 'flight-info')
    if not block:
        return []
    flights = util.fetch_multi(block, 'find_elements_by_class_name',
                                 'section')
    format_flights = []
    for flight in flights:
        info = dig_info(flight)
        if info:
            format_flights.append(info)
    browser.quit()
    return util.deal(period, format_flights, Website.CEAIR, url)

