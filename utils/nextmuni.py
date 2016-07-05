import requests
import xmltodict
import pandas as pd

from utils.database import  read_dataframe_from_postgres
# from utils.database import read_dataframe_from_postgres
from auth.headway_auth import CHARLES_HEADWAY_AUTH


STOPS_BY_ROUTE = (read_dataframe_from_postgres('select route_id, stop_id, xml_tag from stops', CHARLES_HEADWAY_AUTH)
                  .groupby('route_id'))
STOPS_BY_ROUTE = {id: group['xml_tag'].values for id, group in STOPS_BY_ROUTE}

def _construct_predictions_for_multistops_url(route_stop_tuples):
    return ('http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a=sf-muni&' +
            '&'.join('stops=%s|%s' % (x[0], x[1]) for x in route_stop_tuples))

def fetch_predictions_by_route(route_id):
    route_id = str(route_id)
    stop_ids = STOPS_BY_ROUTE[route_id]
    # Hard-coded limit on number of stops per call as per Nextbus API documentation
    stop_id_list = [stop_ids[i:i+150] for i in range(0, len(stop_ids), 150)]
    doclist = []
    for l in stop_id_list:
        doclist.append(xmltodict.parse(
                requests.get(_construct_predictions_for_multistops_url([(route_id, x) for x in l])).text))
    return [x['body'] for x in doclist]

def process_stop_direction(stop, stop_list, direction):
    prediction = direction['prediction'] if type(direction['prediction']) == list else [direction['prediction']]
    stop_list += [
        {
            'route_id': stop['@routeTag'],
            'route_name': stop['@routeTitle'],
            'stop_tag': stop['@stopTag'],
            'stop_name': stop['@stopTitle'],
            'vehicle_id': x['@vehicle'],
            'direction_id': x['@dirTag'],
            'direction_name': direction['@title'],
            'trip_id': x['@tripTag'],
            'arrival_seconds': x['@seconds'],
        }
        for x in prediction
        ]


def fetch_arrivals_dataframe(route_id):

    all_pred = fetch_predictions_by_route(5)

    stop_list = []
    for pred in all_pred:
        for stop in pred['predictions']:
            if 'direction' in stop.keys():
                if type(stop['direction']) == list:
                    for direction in stop['direction']:
                        process_stop_direction(stop, stop_list, direction)
                else:
                    process_stop_direction(stop, stop_list, stop['direction'])
    return pd.DataFrame(stop_list)


if __name__ == '__main__':
    # print(STOPS_BY_ROUTE['5'])
    print(fetch_predictions_by_route('5'))
