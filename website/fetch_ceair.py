#!/usr/bin/env python
# -*- coding: utf-8 -*-
import util
import time
from selenium import webdriver
from constant import Website
from setting.fetch_settings import URL_PARAMS


def dig_info(flight):
    try:
        part1 = flight.find_element_by_class_name('f-i').text
        elements = [x.strip() for x in part1.split('\n')]
        info = elements[0].replace('|', ' ').strip().split()
        airline = info[0].strip() if len(info) >= 1 else ''
        flight_no = info[1].strip() if len(info) >= 2 else ''
        airports = flight.find_elements_by_class_name('airport')
        from_infos = airports[0].text.split()
        to_infos = airports[1].text.split()
        from_time, from_airport = from_infos[0].strip(), from_infos[1].strip()
        to_time, to_airport = to_infos[0].strip(), to_infos[1].strip()

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
        if prices[-1] == 160:
            prices = prices[0:-1]
        if not prices:
            util.log_error(u'CEAIR: 抓取价格失败')
            return None
        price = min(prices)
        if len(prices) >= 2 and price == 160:
            price = prices[-2]
        return [airline, flight_no, from_airport, from_time,
                from_time_pair, to_airport, to_time, to_time_pair, price]
    except Exception as e:
        util.log_error('CEAIR: ' + str(e))
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
    time.sleep(3)
    flights = util.fetch_multi(block, 'find_elements_by_class_name', 'section')
    format_flights = []
    for flight in flights:
        info = dig_info(flight)
        if info:
            format_flights.append(info)
    browser.quit()
    return util.deal(period, format_flights, Website.CEAIR, url)

