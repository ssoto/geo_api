#! /usr/bin/python
# -*- encode: UTF-8 -*-

from datetime import datetime
import psycopg2

from geo_api import settings
from geo_api.utils.common import instanciate_logger
from geo_api.models.air_quality import (Station,
                                        Measure,
                                        Sample,
                                        )

LOGGER = instanciate_logger()

class EntityManager(object):
    """This class will be used as base class of generic class
    database method"""

    def __init__(self):
        conn_str = EntityManager.build_db_string(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db_name=settings.DB_NAME,
        )
        self.conn = psycopg2.connect(conn_str)

    @staticmethod
    def build_db_string(host: str, port: str, db_name:str, user:str,
                        password:str) -> str:
        """Build PostgreSQL connection string

        :return: str with
        """
        return 'host={host} port={port} ' \
               'dbname={dbname} user={user} password={secret}'.format(
            host=host,
            port=port,
            dbname=db_name,
            user=user,
            secret=password,
        )

    def execute_query(self, cursor, query: str) -> object:
        try:
                LOGGER.debug('Connection created...')
                cursor.execute(query)
                self.conn.commit()
        except Exception as e:
            LOGGER.error('Error raised executing query: {}'.format(
                repr(e)
            ))
        return None


class QueryMultipleResultException(Exception):
    pass


class StationEntityManager(EntityManager):

    def create_station(self, station_id: str) -> Station:
        """

        :param station_id:
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(
            '''
                INSERT INTO air_quality__station
                VALUES %s
            ''',
            (station_id, )
        )
        self.conn.commit()

        return Station(station_id)

    def retrieve_station(self, station_id: str) -> Station:
        cursor = self.conn.cursor()

        cursor.execute(
            '''
            SELECT 'station_id'
            FROM air_quality__station
            WHERE 'sation_id'=\'{STATION_ID}\'
            ''',
            (station_id, )
        )
        self.conn.commit()

        row = cursor.fetchone()
        cursor.close()
        station_id = row[0]
        return Station(station_id)


class MeasureEntityManager(EntityManager):

    def create_measure(self, name: str, units: str, sanity_value: float):
        cursor = self.conn.cursor()

        cursor.execute(
            """
                INSERT INTO AIR_QUALITY__MEASURE (name, units, qa)
                VALUES (%s, %s, %s);
            """,
            (name, units, sanity_value)
        )
        self.conn.commit()
        return

    def retrieve_measure(self, name):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT name, units, qa
            FROM AIR_QUALITY__MEASURE
            WHERE name = %s
            """,
            (name, )
        )
        result = cursor.fetchone()
        return Measure(
            name=result[0],
            unit=result[1],
            qa=result[2],
        )


class SampleEntityManager(EntityManager):

    def create_sample(self, measure_name: str, station_id_entity: str, ts: datetime,
                      value: float):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO AIR_QUALITY__SAMPLE (id_station, id_measure, value, ts)
            VALUES (%s, %s, %s, %s)
            """,
            (measure_name,
             station_id_entity,
             value,
             ts
            )
        )
