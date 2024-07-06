import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


class NoArgsError(Exception):
    pass


class NoApiKeyError(Exception):
    pass


def create_headers():
    api_key = os.environ.get('NS_APIKEY')
    if api_key is None:
        raise NoApiKeyError

    return {'Ocp-Apim-Subscription-Key': api_key}


def call_api(origin, destination):
    params = urllib.parse.urlencode({'fromStation': origin, 'toStation': destination})
    url = 'https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips?' + params

    req = urllib.request.Request(url, headers=create_headers())
    response = urllib.request.urlopen(req)
    return json.loads(response.read())


def first_station(trip):
    first_leg = trip['legs'][0]
    return first_leg['origin']


def last_station(trip):
    last_leg = trip['legs'][-1]
    return last_leg['destination']


def duration(time):
    return "%d:%02d" % (time / 60, time % 60)


def format_date(date):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')


def create_title(trip):
    return "%s -> %s\t\t\tDuration: (%s)\tTransfers: %dx" % (
        format_date(first_station(trip)['plannedDateTime']),
        format_date(last_station(trip)['plannedDateTime']),
        duration(trip['plannedDurationInMinutes']),
        trip['transfers']
    )


def product_names(trip):
    transfers = [leg['product']['longCategoryName'] for leg in trip['legs']]
    return ' + '.join(transfers)


def create_subtitle(trip):
    if trip['status'] == 'CANCELLED':
        return "%s\t\t\t%s" % (
            trip['status'],
            product_names(trip)
        )
    else:
        return "Track: %s\t\t\t%s" % (
            first_station(trip)['plannedTrack'],
            product_names(trip)
        )


def new_item_from_trip(trip):
    return {'title': create_title(trip),
            'subtitle': create_subtitle(trip),
            'arg': trip['shareUrl']['uri']}


def extract_arguments():
    try:
        if len(sys.argv) == 3:
            if sys.argv[1] and sys.argv[2]:
                return sys.argv[1], sys.argv[2]
        raise IndexError
    except IndexError:
        raise NoArgsError


def retrieve_schedule():
    try:
        (origin, destination) = extract_arguments()

        response = call_api(origin, destination)
        return [new_item_from_trip(trip) for trip in response['trips']]
    except NoApiKeyError:
        return [{'title': 'Please specify API key in settings'}]
    except NoArgsError:
        return [{'title': 'Please provide origin and destination stations'}]
    except ValueError:
        return [{'title': 'Can\'t parse server response'}]
    except urllib.error.HTTPError:
        return [{'title': 'Error contacting server'}]


def create_json(items):
    return json.dumps({'items': items})


def main():  # pragma: nocover
    print((create_json(retrieve_schedule())))


if __name__ == '__main__':  # pragma: nocover
    main()
