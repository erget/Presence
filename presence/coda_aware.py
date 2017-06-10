"""Tools for dealing with EUMETSAT's CODA server."""

class CODA_Aware(object):

    """
    A class that sends authenticated queries to CODA.
    """

    def __init__(self):
        pass

    def query(self, query_string):
        """Stream authenticated response from CODA OData v1 API."""
        return StreamingResponse
