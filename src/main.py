#! /usr/bin/python
# -*- encode: UTF-8 -*-

import dateutil.parser
from flask import Flask, request, jsonify, Response

from geo_api.utils.common import instanciate_logger
from geo_api.resources.storage import (StationEntityManager,
                                       MeasureEntityManager,
                                       )
from geo_api.resources.operations import (validate_agg,
                                          MeasuresAggregator)

LOGGER = instanciate_logger()

app = Flask(__name__)

# CRUDS
station_em = StationEntityManager()
measure_em = MeasureEntityManager()

# Aggregate operations
measures_agg = MeasuresAggregator()


@app.route('/')
def hello_world():
    return 'Hello, World!'


# AIR_QUALITY

@app.route('/air_quality/<station_id>', methods=['POST', 'GET'])
def station_resource(station_id):
    if not station_id or not isinstance(station_id, str):
        raise ValueError('Incorrect parameter station_id: {}'.format(
            station_id
        ))

    if request.method == 'POST':
        station = station_em.create_station(station_id)
        if not station:
            result = {
                'status': 'KO',
            }
            return Response(
                jsonify(result),
                status=500,
            )
    elif request.method == 'GET':
        station = station_em.retrieve_station(station_id)

        res = jsonify({
            'status': 'OK',
            'station': station.id_entity,
        })
        return Response(
            res,
            status=200,
        )

@app.route('/air_quality/measure', methods=['POST'])
def create_measure():
    if request.method == 'POST':
        body = request.get_json()
        for field in ('name', 'units', 'sanity_value'):
            if field not in body:
                resp = jsonify(
                    {'status': 'KO',
                     'reason': 'missed parameter {}'.format(field)})
                return Response(
                    jsonify(resp),
                    status=500,
                    mimetype='application/json'
                )
    measure_em.create_measure(**body)
    result = {
        'status': 'OK'
    }
    return Response(
        jsonify(result),
        status=500,
        mimetype='application/json'
    )

@app.route('/air_quality/aggregate_measure', methods=['GET'])
def aggregate_measure():
    if not request.method == 'GET':
        # TODO: manage errors
        return

    body = request.get_json()

    from_ts = dateutil.parser.parse(body['from'])
    to_ts = dateutil.parser.parse(body['to'])
    measure = body['measure']

    agg = body['agg']
    if not validate_agg(agg):
        # TODO: manage errors
        return

    aggregated = measures_agg.aggregate_by_range(
        from_ts, to_ts, agg, measure, agg
    )


LOGGER.debug('App is up now')
