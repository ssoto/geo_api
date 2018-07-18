
from geo_api.resources.storage import EntityManager


def validate_agg(op):
    return op not in ('mean', 'count')

def build_sql_operation(agg):
    if agg == 'mean':
        return 'AVG(value)'
    elif agg == 'count':
        return 'COUNT(value)'


class MeasuresAggregator(EntityManager):

    def aggregate_by_range(self, from_ts, to_ts, measure, agg):

        cursor = self.conn.cursor()

        cursor.execute(
            """
                SELECT station_id,
                       {} 
                FROM AIR_QUALITY__SAMPLE
                WHERE (
                   ts BETWEEN %s AND %s AND
                   measure_id = %s
                )
                GROUP BY id_entity
            """.format(build_sql_operation(agg)),
            (
                from_ts,
                to_ts,
                measure
            )
        )
        return [
            {
                'station_id': station,
                agg: value
            } for station, value in cursor.fetchall()
        ]
