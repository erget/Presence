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

    def __init__(self, prod_type, time_start, time_end, intersect_geom):
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
        self.uuids = []

    def get_uuids(self, limit=None):
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

        filters = product_filter + time_filter + geom_filter

        results = []
        found_results = [True]
        skip = 0
        # We iterate because API only returns limited number of UUIDs
        while found_results:
            query = "Products?$skip={}&$filter={}&$format=json".format(
                skip, filters)
            json_results = json.loads(self.query(query).text)
            try:
                found_results = [product["Id"] for product in json_results[
                    "d"]["results"]]
            except KeyError:
                found_results = []
            results += found_results
            skip += len(found_results)
            if limit is not None:
                if skip > limit:
                    found_results = []
        return results


if __name__ == '__main__':
    q = Query("SR_2_WAT", datetime(2017, 2, 1), datetime(2017, 2, 2), None)
    q = Query("OL_1", datetime(2017, 2, 1), datetime(2017, 2, 3), None)
    q.get_uuids()
