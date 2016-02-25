#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import util
from selenium import webdriver


def dig_info(flight):
    try:
        if len(flight.find_elements_by_class_name('colAirports')) != 1:
            return None
        from_airport, to_airport = flight.\
            find_elements_by_class_name('colAirports')[0].\
            text.strip().split('-')
        info = flight.find_element_by_class_name('colFlight').text.\
            strip()
        from_time = flight.find_element_by_class_name('colDepart').text.\
            strip()[0:5]
        to_time = flight.find_element_by_class_name('colArrive').text.\
            strip()[0:5]
        prices = [int(x.text.strip().replace(',', '')) for x
                  in flight.find_elements_by_class_name('colPrice')]
        if not prices:
            return None
        price = min(prices)
        from_time_pair = [int(x) for x in from_time.split(':')]
        to_time_pair = [int(x) for x in to_time.split(':')]
        if to_time_pair[0] < from_time_pair[0]:
            to_time_pair[0] += 24
        return [info, from_airport, from_time,
                from_time_pair, to_airport, to_time, to_time_pair, price]
    except Exception as e:
        return None


def fetch(period):
    format_flights = []
    airport_pairs = [(x, y) for x in period['from_airport']
                     for y in period['to_airport']]
    origin_url = 'http://et.airchina.com.cn/cn/index.shtml'
    for pair in airport_pairs:
        browser = webdriver.PhantomJS()
        date = period['date']
        url = 'http://et.airchina.com.cn/InternetBooking/AirLowFareSearchExternal' \
            '.do?tripType=OW&searchType=FARE&flexibleSearch=false' \
            '&directFlightsOnly=false&fareOptions=1.FAR.X' \
            '&outboundOption.originLocationCode=' + \
                        URL_PARAMS[Website.CSAIR][pair[0]] + \
            '&outboundOption.destinationLocationCode=' + \
                        URL_PARAMS[Website.CSAIR][pair[1]] + \
            '&outboundOption.departureDay=' + date[8:] + \
            '&outboundOption.departureMonth=' + date[5:7] + \
            '&outboundOption.departureYear=' + date[0:4] + \
            '&outboundOption.departureTime=NA' \
            '&guestTypes%5B0%5D.type=ADT' \
            '&guestTypes%5B0%5D.amount=1' \
            '&guestTypes%5B1%5D.type=CNN' \
            '&guestTypes%5B1%5D.amount=0' \
            '&guestTypes%5B2%5D.type=INF' \
            '&guestTypes%5B2%5D.amount=0' \
            '&pos=AIRCHINA_CN&lang=zh_CN'
        browser.get(url)
        block = util.fetch_one(browser, 'find_element_by_id',
                               'resultsFFBlock1')
        if not block:
            continue
        flights = util.fetch_multi(block, 'find_elements_by_tag_name',
                                   'tbody')
        for flight in flights:
            info = dig_info(flight)
            if info:
                format_flights.append(info)
        browser.quit()
    return util.deal(period, format_flights, Website.AIRCHINA, origin_url)

