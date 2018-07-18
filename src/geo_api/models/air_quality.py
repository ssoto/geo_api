#! /usr/bin/python
# -*- encode: UTF-8 -*-

from datetime import datetime

class Station:

    def __init__(self, id_entity: str):
        self.id_entity = id_entity


class Measure:

    def __init__(self, name:str, unit: str, qa: float):
        self.name = name
        self.unit = unit
        self.qa = qa


class Sample:

    def __init__(self, station: Station, measure: Measure,
                 timestamp: datetime, value: float):
        self.station = station
        self.measure = measure
        self.datetime = timestamp
        self.value = value
