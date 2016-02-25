#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import util
import requests
import json


def dig_info(flight):
    try:
        number = flight['No']
        from_airport = flight['Departure'] + flight['DepartureStation']
        from_time = flight['DepartureTime'][11:16]
        to_airport = flight['Arrival'] + flight['ArrivalStation']
        to_time = flight['ArrivalTime'][11:16]
        prices = [x['Cabins'][0]['CabinPrice'] for x in flight['CabinInfos'] if
                  x.get('Cabins') and
                  isinstance(x['Cabins'][0].get('CabinPrice'), int)]
        if not prices:
            return None
        from_time_pair = [int(x) for x in from_time.split(':')]
        to_time_pair = [int(x) for x in to_time.split(':')]
        if to_time_pair[0] < from_time_pair[0]:
            to_time_pair[0] += 24
        price = min(prices)
        return [number, from_airport, from_time,
                from_time_pair, to_airport, to_time, to_time_pair, price]
    except Exception as e:
        return None


def fetch(period):
    url = u'http://flights.ch.com/default/SearchByTime?Stype=0&IfRet=false&' \
          u'OriCity=%s&DestCity=%s&MType=0&FDate=%s' \
          u'&ANum=1&CNum=0&INum=0&PostType=0' % (
              URL_PARAMS[Website.QUNAR][period['from_city']][0],
              URL_PARAMS[Website.QUNAR][period['to_city']][0],
              period['date'],
          )
    response = requests.post(url)
    try:
        msg = json.loads(response.text)
        flights = [x[0] for x in msg['Packages'] if len(x) == 1]
    except:
        return []
    format_flights = []
    for flight in flights:
        info = dig_info(flight)
        if info:
            format_flights.append(info)
    log_url = u'http://flights.ch.com/SHA-CKG.html?IfRet=false' \
              u'&OriCity=%s&OriCode=%s&DestCity=%s&DestCode=%s&FDate=%s' \
              u'&MType=0&ANum=1&CNum=0&INum=0&SType=0' % (
                  URL_PARAMS[Website.QUNAR][period['from_city']][0],
                  URL_PARAMS[Website.QUNAR][period['from_city']][1],
                  URL_PARAMS[Website.QUNAR][period['to_city']][0],
                  URL_PARAMS[Website.QUNAR][period['to_city']][1],
                  period['date'],
              )
    return util.deal(period, format_flights, Website.CH, log_url)
