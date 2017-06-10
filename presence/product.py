"""Abstraction for dealing with products and the files they contain."""

import os
from xml.dom.minidom import parseString

from .coda_aware import CODA_Aware

class Product(CODA_Aware):

    """A CODA product, composed mainly of NetCDF files."""

    def __init__(self, uuid):
        self.uuid = uuid
        uuid_query = "Products('{}')".format(self.uuid)
        res = self.query(uuid_query)
        dom = parseString(res.text)

        nodes = self.query(uuid_query + "/Nodes")
        dom = parseString(nodes.text)
        self.root = dom.getElementsByTagName("title").item(
            1).firstChild.nodeValue

        manifest_query = (uuid_query +
                          "/Nodes('{}')/Nodes("
                          "'xfdumanifest.xml')/$value".format(self.root))
        manifest = parseString(self.query(manifest_query).text)
        self.files = [x.attributes.get("href").nodeValue for x in
                      manifest.getElementsByTagName("fileLocation")]

        try:
            os.makedirs(self.root)
        except FileExistsError:
            pass


    def get(self, filename):
        """If needed, retrieve, and return absolute path to file."""
        path = os.path.join(self.root, filename)
        if not os.path.exists(path):
            pass  # Get the file from the server and put it there
        else:
            return path

        """
        You can turn the manifest query into something more general and just
        use it in order to get the node xfdumanifest.xml.
        """