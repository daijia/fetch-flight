#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import util
from selenium import webdriver


def dig_info(flight):
    try:
        info = flight.find_element_by_class_name('logo').text
        divs = flight.find_element_by_class_name('right').\
            find_elements_by_tag_name('div')
        from_time = divs[0].find_element_by_class_name('time').text
        from_time_pair = [int(x) for x in from_time.split(':')]
        from_airport = divs[1].text

        divs = flight.find_element_by_class_name('left').\
            find_elements_by_tag_name('div')
        to_time = divs[0].find_element_by_class_name('time').text
        to_time_pair = [int(x) for x in to_time.split(':')]
        to_airport = divs[1].text
        if to_time_pair[0] < from_time_pair[0]:
            to_time_pair[0] += 24
        price = flight.find_element_by_class_name('price').text[1:]
        tmp_price = ''
        for ch in price:
            if ch.isdigit():
                tmp_price += ch
            else:
                break
        price = int(tmp_price)
        return [' '.join(info.split()), from_airport, from_time,
                from_time_pair, to_airport, to_time, to_time_pair, price]
    except Exception as e:
        return None


def fetch(period):
    browser = webdriver.PhantomJS()
    url = 'http://flights.ctrip.com/booking/%s-%s-day-1.html#DDate1=%s' % \
        (URL_PARAMS[Website.CTRIP][period['from_city']],
         URL_PARAMS[Website.CTRIP][period['to_city']],
         period['date'])
    browser.get(url)
    util.scroll(browser)
    block = util.fetch_one(browser, 'find_element_by_id', 'J_flightlist2')
    if not block:
        return []
    flights = util.fetch_multi(block, 'find_elements_by_class_name',
                                 'search_table_header')
    format_flights = []
    for flight in flights:
        info = dig_info(flight)
        if info:
            format_flights.append(info)
    browser.quit()
    return util.deal(period, format_flights, Website.CTRIP, url)
