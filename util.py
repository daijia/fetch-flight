#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import logging

from constant import AVAILABLE_WEBSITES, Airport, EXEC_TIME
from setting.subscribe_settings import PRICE_FLUCTUATION
from setting.fetch_settings import AIRPORT_NAME_PARAMS
from model.flight import Flight

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    filename='flight.log', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def send_email(content):
    sender = 'xxx@sina.com'
    receiver = 'xxx@163.com'
    subject = '机票查询服务'
    smtpserver = 'smtp.sina.com'
    username = 'xxx@sina.com'
    password = 'xxx'

    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def equal_to(value):
    return lambda x: x == value


def less_than(value):
    return lambda x: x < value


def retry(times, retry_func=None, interval=1):
    def real_decorator(fn):
        def wrap(*args, **kwargs):
            if retry_func:
                for index in range(times-1):
                    try:
                        result = fn(*args, **kwargs)
                        if retry_func(result):
                            if interval:
                                time.sleep(interval)
                            continue
                    except:
                        if interval:
                            time.sleep(interval)
                        continue
                    return result
                return fn(*args, **kwargs)
            else:
                for index in range(times):
                    fn(*args, **kwargs)
                return None
        return wrap
    return real_decorator


def get_week_day(a):
    return {0: u'星期一', 1: u'星期二', 2: u'星期三', 3: u'星期四', 4: u'星期五',
            5: u'星期六', 6: u'星期日', }[
        date(int(a[0:4]), int(a[5:7]), int(a[8:])).weekday()]


def scroll(browser):
    for index in range(0, 10):
        browser.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(0.3)


@retry(10, equal_to(None))
def fetch_one(browser, func_name, value):
    return getattr(browser, func_name)(value)


@retry(8, equal_to([]))
def fetch_multi(block, func_name, value):
    return getattr(block, func_name)(value)


def log_error(msg):
    logging.log(logging.ERROR, str(msg))


def log_info(msg):
    logging.log(logging.INFO, str(msg))


def deal(period, flights, website, url):
    flights = sorted(flights, key=lambda x: x[-1])
    for flight in flights:
        airline, flight_no, from_airport_name, from_time, from_time_pair, \
            to_airport_name, to_time, to_time_pair, price = flight
        if to_time_pair[0] - from_time_pair[0] > 6:
            log_info('long trip '+str(period)+' '+url+' '+str(flight))
            continue
        if not from_airport_name or not to_airport_name:
            log_info('empty airport '+str(period)+' '+url+' '+str(flight))
            continue
        from_airport, to_airport = None, None
        for x in Airport.ALL:
            if AIRPORT_NAME_PARAMS[website][x] in from_airport_name:
                from_airport = x
                break
        for x in Airport.ALL:
            if AIRPORT_NAME_PARAMS[website][x] in to_airport_name:
                to_airport = x
                break
        if from_airport is None or to_airport is None:
            log_info('not found airport '+str(period)+' '+url+' '+str(flight))
            continue
        Flight.insert(from_airport=from_airport,
                      to_airport=to_airport,
                      from_time=from_time,
                      to_time=to_time,
                      from_city=period['from_city'],
                      to_city=period['to_city'],
                      website=website,
                      price=price,
                      flight_date=period['date'],
                      airline=airline,
                      flight_no=flight_no,
                      url=url,
                      fetch_time=EXEC_TIME)


def deal2(period, flights, website, url):
    flights = sorted(flights, key=lambda x: x[-1])
    selected_flights = []
    for flight in flights:
        info, from_airport, from_time, from_time_pair, to_airport, to_time, \
            to_time_pair, price = flight
        begin_time = period.get('begin_time')
        if to_time_pair[0] - from_time_pair[0] > 6:
            continue
        if not from_airport or not to_airport:
            continue
        if begin_time:
            if not ([int(x) for x in begin_time[0].split(':')]
                    <= from_time_pair <=
                    [int(x) for x in begin_time[1].split(':')]):
                continue
        end_time = period.get('end_time')
        if end_time:
            if not ([int(x) for x in end_time[0].split(':')]
                    <= to_time_pair <=
                    [int(x) for x in end_time[1].split(':')]):
                continue

        for x in period['from_airport']:
            if AIRPORT_NAME_PARAMS[website][x] in from_airport:
                from_airport = x
                break
        for x in period['to_airport']:
            if AIRPORT_NAME_PARAMS[website][x] in to_airport:
                to_airport = x
                break

        flight[1], flight[4] = from_airport, to_airport
        selected_flights.append(flight)
    return [(period['date'], website, url, x) for x in selected_flights]



def get_price_trend(period):
    flights = Flight.select(from_city=period['from_city'],
                            to_city=period['to_city'],
                            flight_date=period['date'])
    result = {'all': _get_price_trend(flights)}
    for website in AVAILABLE_WEBSITES:
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