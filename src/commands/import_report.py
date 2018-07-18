#! /usr/bin/python
# -*- encode: UTF-8 -*-
import csv
import argparse
import dateutil.parser

from geo_api.resources.storage import (MeasureEntityManager,
                                       StationEntityManager,
                                       SampleEntityManager,)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-file', help='Report file path'
    )

    args = parser.parse_args()

    measure_em = MeasureEntityManager()
    station_em = StationEntityManager()
    sample_em = SampleEntityManager()

    with open(args.file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            measure_id = int(row['id'])
            ts = dateutil.parser.parse(row['TimeInstant'])
            so2 = float(row['so2'])
            no2 = float(row['no2'])
            pm10 = float(row['pm10'])
            pm2_5 = float(row['pm2_5'])
            co = float(row['co'])
            o3 = float(row['o3'])
            id_entity = row['id_entity']
            created_at = dateutil.parser.parse(row['created_at'])
            updated_at = dateutil.parser.parse(row['updated_at'])

            station = station_em.retrieve_station(
                station_id=id_entity
            )
            measures = (
                (so2, 'so2'),
                (no2, 'no2'),
                (pm10, 'pm10'),
                (pm2_5, 'pm2_5'),
                (co, 'pm2_5'),
                (o3, 'co2'),
            )
            for value, name in measures:
                measure = sample_em.create_sample(
                    name,
                    station_id_entity=station.id_entity,
                    value=value,
                    ts=ts
                )
