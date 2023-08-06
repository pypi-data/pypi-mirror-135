"""pygeoapi implementation of getxsatendpts."""
import logging
import time

from geopandas import GeoDataFrame
from pygeoapi.process.base import BaseProcessor

from nldi_xstool.nldi_xstool import getxsatendpts

# from typing import Any
# from typing import Tuple


LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "nldi-xsatendpts",
    "title": "NLDI xsatendpts process",
    "description": "NLDI xsatendpts process",
    "keywords": ["NLDI xsatendpts"],
    "links": [
        {
            "type": "text/html",
            "rel": "canonical",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-US",
        }
    ],
    "inputs": [
        {
            "id": "lat",
            "title": "lat",
            "input": {
                "literalDataDomain": {
                    "dataType": "list",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 2,
            "maxOccurs": 2,
        },
        {
            "id": "lon",
            "title": "lon",
            "input": {
                "literalDataDomain": {
                    "dataType": "list",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 2,
            "maxOccurs": 2,
        },
        {
            "id": "numpts",
            "title": "numpts",
            "input": {
                "literalDataDomain": {
                    "dataType": "int",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        {
            "id": "3dep_res",
            "title": "resolution",
            "abstract": "Resolution of 3dep elevation data",
            "minOccurs": 1,
            "maxOccurs": 1,
            "input": {
                "literalDataDomain": {
                    "dataType": "enum",
                    "valueDefinition": {
                        "anyValue": False,
                        "defaultValue": "10",
                        "possibleValues": ["30", "10", "5", "3", "1"],
                    },
                }
            },
        },
    ],
    "outputs": [
        {
            "id": "nldi-xsatendpts-response",
            "title": "output nldi-xsatendpts",
            "output": {"formats": [{"mimeType": "application/json"}]},
        }
    ],
    "example": {
        "inputs": [
            {"id": "lat", "value": [40.267720, 40.270568], "type": "text/plain"},
            {"id": "lon", "value": [-103.801086, -103.80097], "type": "text/plain"},
            {"id": "numpts", "value": "101", "type": "text/plain"},
            {"id": "3dep_res", "value": "1", "type": "text/plain"},
        ]
    },
}


class NLDIxsatendptsProcessor(BaseProcessor):  # type: ignore
    """NLDI xsatendpoints Processor."""

    def __init__(self, provider_def):  # type: ignore
        """Initialize object.

        :param provider_def: provider definition
        :returns: pygeoapi.process.nldi_delineate.NLDIDelineateProcessor
        """
        BaseProcessor.__init__(self, provider_def, PROCESS_METADATA)

    def execute(self, data):  # type: ignore
        """Execute processor."""
        print("before data assign")
        print(data)
        # reformat data into dict with just needed values
        newdata = {d["id"]: d["value"] for d in data}
        mimetype = "application/json"
        lat = newdata.get("lat")
        lon = newdata.get("lon")
        numpts = int(newdata.get("numpts"))  # type: ignore
        res = int(newdata.get("3dep_res"))  # type: ignore

        print(lat, lon, numpts, res)

        timebefore = time.perf_counter()

        print("before function")
        results = GeoDataFrame(
            getxsatendpts(
                path=[(lon[0], lat[0]), (lon[1], lat[1])],  # type: ignore
                numpts=numpts,
                res=res,
                crs="epsg:4326",
            )
        )
        print("after function")
        # print(results)

        timeafter = time.perf_counter()
        totaltime = timeafter - timebefore
        print("Total Time:", totaltime)

        # outputs = [
        #     {"id": "nldi-xsatendpts-response", "value": results.__geo_interface__}
        # ]
        # print(results)
        return mimetype, results.__geo_interface__

    def __repr__(self):  # type: ignore
        """Get representation."""
        return "<NLDIxsatendptsProcessor> {}".format("get xsatendpts")
