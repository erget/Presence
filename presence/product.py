"""Abstraction for dealing with products and the files they contain."""

import os
from xml.dom.minidom import parseString

from .coda_aware import CODA_Aware

class Product(CODA_Aware):

    """A CODA product, composed mainly of NetCDF files."""

    def __init__(self, uuid, work_dir=""):
        self.files = []
        self.work_dir = work_dir
        self.uuid = uuid
        uuid_query = "Products('{}')".format(self.uuid)

        nodes = self.query(uuid_query + "/Nodes")
        dom = parseString(nodes.text)
        self.root = dom.getElementsByTagName("title").item(
            1).firstChild.nodeValue

        try:
            os.makedirs(os.path.join(work_dir, self.root))
        except FileExistsError:
            pass

        manifest_file = self.get("xfdumanifest.xml")
        with open(manifest_file) as manifest:
            manifest_dom = parseString(manifest.read())
        self.files = [x.attributes.get("href").nodeValue[2:] for x in
                      manifest_dom.getElementsByTagName("fileLocation")]

    def get(self, filename):
        """If needed, retrieve, and return absolute path to file."""
        if self.files and not filename in self.files:
            raise FileNotFoundError("The requested file is not part of this "
                                    "product.")
        path = os.path.join(self.work_dir, self.root, filename)
        if not os.path.exists(path):
            # Get the file from the server and put it there
            result = self.query("Products('{}')/Nodes('{}')/Nodes('{"
                                "}')/$value".format(self.uuid, self.root,
                                                    filename))
            with open(path, "wb") as f:
                for chunk in result.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        return os.path.abspath(path)

