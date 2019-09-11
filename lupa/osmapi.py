import requests
import urllib

OSM_APY = "http://photon.komoot.de/api/"

BASE_PROPS = {
    "q": "",
}

MIN_LAT = -44.8872118186704
MAX_LAT = -40.9597503622894
MIN_LON = -23.3668677850202
MAX_LON = -20.7649623309468


class QueryController:
    def _query(self, terms):
        basereq = BASE_PROPS.copy()
        basereq['q'] = terms

        basereq = urllib.parse.urlencode(basereq)

        response = requests.get(OSM_APY + "?" + basereq)

        return response.json()

    def _filter_response(self, features):
        def filter_bbox(feature):
            coords = feature['geometry']['coordinates']
            return MIN_LAT <= coords[0] <= MAX_LAT and\
                MIN_LON <= coords[1] <= MAX_LON

        return list(filter(filter_bbox, features))

    def query(self, terms):
        return [
            OsmQuery(item)
            for item in
            self._filter_response(
                self._query(
                    terms
                )["features"]
            )
        ]


class OsmQuery:
    objects = QueryController()

    def __init__(self, feature):
        self.feature = feature
