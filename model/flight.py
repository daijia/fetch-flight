#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataset
import time


class Flight(object):

    db = dataset.connect('sqlite:///db_flight')
    table = db['tb_flight']
    __necessary_fields__ = ['from_airport', 'to_airport', 'from_city',
                            'to_city', 'from_time', 'to_time', 'website',
                            'price', 'flight_date', 'fetch_time']
    __fields__ = ['id', 'from_airport', 'to_airport', 'from_city', 'to_city',
                  'from_time', 'to_time', 'website', 'price', 'flight_date',
                  'airline', 'flight_no', 'url', 'fetch_time']

    @classmethod
    def insert(cls, **kwargs):
        for field in ['airline', 'flight_no', 'url']:
            kwargs[field] = kwargs.get(field) if kwargs.get(field) else ''
        for f in Flight.__necessary_fields__:
            if f not in kwargs:
                raise ValueError
        for key in kwargs:
            if key not in Flight.__fields__:
                print key
                raise ValueError
        kwargs['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime())
        return Flight.table.insert(kwargs)

    @classmethod
    def select(cls, **kwargs):
        flights = Flight.table.find(**kwargs)
        result = list()
        for flight in flights:
            tmp = dict()
            for key in Flight.__fields__:
                tmp[key] = flight[key]
            result.append(tmp)
        return result

    @classmethod
    def get_last_fetch_time(cls):
        flights = Flight.table.find(order_by=['-fetch_time'], _limit=1)
        if not flights:
            return None
        for flight in flights:
            return flight['fetch_time']