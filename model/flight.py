#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataset
import time
import uuid


class Flight(object):

    db = dataset.connect('sqlite:///:db_flight:')
    table = db['tb_flight']
    __necessary_fields__ = ['from_airport', 'to_airport', 'from_city',
                            'to_city', 'from_time', 'to_time', 'website',
                            'price', 'flight_date', 'time_range', 'fetch_time']
    __fields__ = ['from_airport', 'to_airport', 'from_city', 'to_city',
                  'from_time', 'to_time', 'website', 'price', 'flight_date',
                  'detail', 'url', 'time_range', 'fetch_time']

    @classmethod
    def insert(cls, **kwargs):
        kwargs['detail'] = kwargs.get('detail') if kwargs.get('detail') else ''
        kwargs['url'] = kwargs.get('url') if kwargs.get('url') else ''
        for f in Flight.__necessary_fields__:
            if f not in kwargs:
                raise ValueError
        for key in kwargs:
            if key not in Flight.__fields__:
                print key
                raise ValueError
        kwargs['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime())
        kwargs['unique_id'] = uuid.uuid4().get_hex()
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