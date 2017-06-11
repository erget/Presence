import json
from .coda_aware import CODA_Aware
from datetime import datetime


class Query(CODA_Aware):
    """Find CODA products based on search criteria."""

    def _datetime_to_filter_string(self, dt, cmp):
        str = "IngestionDate " + cmp + dt.strftime("datetime'%Y-%m%dT%I:%M:%S'")
        return str

    def __init__(self, time_start, time_end, bbox, prod_type):
        self.time_start = time_start
        self.time_end = time_end
        self.bbox = bbox,
        self.prod_type = prod_type
        if not self._prod_type_is_valid():
            raise ()
        self.uuids = []

    def _prod_type_is_valid(self):
        return True

    def get_uuids(self):
        product_filter = "substringof('" + self.prod_type + "',Name)"
        ge_filter = self._datetime_to_filter_string(self.time_start, "ge")
        le_filter = self._datetime_to_filter_string(self.time_end, "le")
        time_filter = ge_filter + " AND " + le_filter
        query = "Products?&filter=" + product_filter + time_filter + "&$format=json"
        found_results = [product["Id"] for product in json.loads(self.query(
            query).text)["d"]["results"]]
        return found_results


if __name__ == '__main__':
    q = Query(datetime(2017, 1, 1), datetime(2017, 1, 2), None, "_SR_2_WAT_")
    print(q.get_uuids())
