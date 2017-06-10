"""Tools for dealing with EUMETSAT's CODA server."""

import requests
from requests.auth import HTTPBasicAuth


class CODA_Aware(object):

    """
    A class that sends authenticated queries to CODA.
    """

    #: Authentification details. This should be configured, not in sources!
    user = "hackathon12"
    password = "copernicus"
    SERVICE_ROOT = "https://coda.eumetsat.int/odata/v1/"

    def __init__(self):
        pass #raise NotImplementedError()

    def query(self, query_string):
        """Stream authenticated response from CODA OData v1 API."""
        return requests.get(self.SERVICE_ROOT + query_string,
                            auth=HTTPBasicAuth(self.user, self.password),
                            verify=False, stream=True)
