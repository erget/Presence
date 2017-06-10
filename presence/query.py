import json
from .coda_aware import CODA_Aware
from datetime import datetime

class Query(CODA_Aware):

    def __init__(self, time_start, time_end, bbox, prod_type):
        self.time_start = time_start
        self.time_end = time_end
        self.bbox = bbox,
        self.prod_type = prod_type
        if not self.prod_type_is_valid():
            raise()
        self.uuids = []


    def prod_type_is_valid(self):
        return True

    def get_uuids(self):
        uuids = []

        product_filter = "substringof('" + self.prod_type +"',Name)"
        time_filter = datetime_to_filter_string(self.time_start, "gt") + " AND " + datetime_to_filter_string(self.time_end, "lt")
        query = "Products?&filter=" + product_filter + time_filter + "&$format=json"
        print("Query: " + query)
        found_results = json.loads(self.query(query).text)
        return found_results


def datetime_to_filter_string(dt, cmp):
    return "year(IngestionDate) " + cmp + " " + dt.year +\
           " and month(IngestionDate) " + cmp + " " + dt.month +\
           " and day(IngestionDate) " + cmp + " " + dt.day +\
           " and hour(IngestionDate) " + cmp + " " + dt.hour + \
           " and minute(IngestionDate) " + cmp + " " + dt.minute + \
           " and second(IngestionDate) " + cmp + " " + dt.second


if __name__ == '__main__':
    q = Query(datetime(2017,1,1), datetime(2017,1,2), None, "_SR_2_WAT_")
    print( q.get_uuids() )