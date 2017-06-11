import json
from .coda_aware import CODA_Aware
from datetime import datetime


def datetime_to_filter_string(dt, cmp):
    """Create filter string from datetime."""
    ret = ""
    if dt is not None:
        ret = "IngestionDate " + cmp + dt.strftime(" datetime'%Y-%m-%dT%I:%M:%S'")
    return ret


def geom_to_filter_string(bbox):
    """Create filter string from GML polygon."""
    if bbox is not None:
        res = 'footprint:"Intersects({})"'.format(bbox)
    else:
        res = ""
    return ""


class Query(CODA_Aware):
    """Find CODA products based on search criteria."""

    def __init__(self, time_start, time_end, intersect_geom, prod_type):
        """
        Construct OData REST query for CODA to find matching products.

        :param time_start: datetime of earliest data to be returned
        :param time_end: datetime of most recent data to be returned
        :param intersect_geom: Intersecting geometry in WGS84. Disabled.
        :param prod_type: Product type substring as defined in CODA user guide

        intersect_geom is currently not used due to questions concerning the
        API.
        """
        self.time_start = time_start
        self.time_end = time_end
        self.prod_type = prod_type
        self.geom_filter = intersect_geom
        if not self._prod_type_is_valid():
            raise ()
        self.uuids = []

    def _prod_type_is_valid(self):
        return True

    def get_uuids(self):
        product_filter = "substringof('" + self.prod_type + "',Name)"

        ge_filter = datetime_to_filter_string(self.time_start, "ge")
        le_filter = datetime_to_filter_string(self.time_end, "le")
        if ge_filter and le_filter:
            time_filter = ge_filter + " and " + le_filter
        elif ge_filter or le_filter:
            time_filter = ge_filter + le_filter
        if time_filter:
            time_filter = " and " + time_filter

        geom_filter = geom_to_filter_string(self.geom_filter)
        if geom_filter:
            geom_filter = " and " + geom_filter

        query = "Products?&$filter=" + product_filter + time_filter\
                + geom_filter + "&$format=json"
        print(query)
        found_results = [product["Id"] for product in json.loads(self.query(
            query).text)["d"]["results"]]
        return found_results
    # iterate over results and return when empty becaues of query limits


if __name__ == '__main__':
    q1 = Query(datetime(2017, 2, 2, 1), datetime(2017, 2, 2, 2), "foo", "SR_2_WAT")
    q2 = Query(datetime(2017, 2, 1), datetime(2017, 2, 2), "SR_2_WAT")
    print(len(q1.get_uuids()))
    print(len(q2.get_uuids()))

    q1 = Query(datetime(2017, 2, 2, 1), datetime(2017, 2, 2, 2), None, "SR_2_WAT")
    q1 = Query(datetime(2017, 2, 2, 1), datetime(2017, 2, 2, 2), polysad, "SR_2_WAT")
    print(len(q1.get_uuids()))
