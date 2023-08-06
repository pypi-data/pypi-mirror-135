"""Main module."""
# from nldi_xstool.cli import xsatendpts
import sys
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import py3dep
import requests
from pynhd import NLDI
from shapely.geometry import LineString
from shapely.geometry import Point

from .PathGen import PathGen
from .XSGen import XSGen


def dataframe_to_geodataframe(
    df: pd.DataFrame, crs: str
) -> gpd.GeoDataFrame:  # noqa D103
    """Convert pandas Dataframe to Geodataframe."""
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    df = df.drop(["x", "y"], axis=1)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    return gdf


def get_elev_along_path(
    path: List[Tuple[float, float]],
    numpts: int,
    crs: Optional[str] = "epsg:4326",
    file: Optional[str] = None,
    res: Optional[int] = 10,
) -> Union[int, gpd.GeoDataFrame]:
    """Get elevation at user-defined path.

    Note 1:
        Cross-section is interpolated using 3DEP elevation services which does not
        include bathymetric data.

    Note 2:
        The parameter res specifices the spatial resolution of the 3DEP data that is
        interpolated to return elevation values of the cross-section points.  It does
        not specify the native spatial resolution of the 3DEP data.  If using this as a
        package the query_dems function in nldi-xstool.ancillary can be used to discover
        the available native resolution of the 3DEP data at the bounding box of the
        cross-section.

    Args:
        path (List[Tuple[float, float]]): List of tuples containing coordinate pairs
            of the path, for example: [(x1,y1), (x2,y2), (x3, y3)]
        numpts (int): Number of points to interpolate along path.
        crs (Optional[str], optional): crs of input data. Defaults to "epsg:4326".
        file (Optional[str], optional): path/to/file.json. Defaults to None and returns
            a GeoDataFrame.
        res (Optional[int], optional): Spatial resolution of 3DEP Dem data. Defaults to
            10 which is available throughout CONUS.

    Returns:
        Union[int, gpd.GeoDataFrame]: If a file is specified it writes a json file and
            returns 0, otherwise it returns the cross-section in a GeoDataFrame.
    """
    lnst = []
    for pt in path:
        lnst.append(Point(pt[0], pt[1]))

    # print(ls1)
    d = {"name": ["xspath"], "geometry": [LineString(lnst)]}
    gpd_pth = gpd.GeoDataFrame(d, crs=crs)
    # print(gpd_pth)
    gpd_pth.to_crs(epsg=3857, inplace=True)
    # print(gpd_pth)
    xs = PathGen(path_geom=gpd_pth, ny=numpts)
    xs_line = xs.get_xs()
    # print(xs_line.head())
    # print(xs_line.total_bounds, xs_line.bounds)
    bb = xs_line.total_bounds - ((100.0, 100.0, -100.0, -100.0))
    # print('before dem', bb)
    dem = py3dep.get_map(
        "DEM", tuple(bb), resolution=res, geo_crs="EPSG:3857", crs="epsg:3857"
    )
    # print('after dem')
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=("z", x), y=("z", y))
    pdsi = dsi.to_dataframe()
    gpdsi = dataframe_to_geodataframe(pdsi, crs="epsg:3857")
    gpdsi["distance"] = _get_dist_path(gpdsi)
    gpdsi.to_crs(epsg=4326, inplace=True)
    if file:
        with open(file, "w") as f:
            f.write(gpdsi.to_json())
            f.close()
            return 0
    else:
        return gpdsi


def getxsatendpts(
    path: List[Tuple[float, float]],
    numpts: int,
    crs: Optional[str] = "epsg:4326",
    file: Optional[str] = None,
    res: Optional[int] = 10,
) -> Union[int, gpd.GeoDataFrame]:
    """Get cross-section at user defined endpoints.

    Note 1:
        Cross-section is interpolated using 3DEP elevation services which does not
        include bathymetric data.

    Note 2:
        The parameter res specifices the spatial resolution of the 3DEP data that is
        interpolated to return elevation values of the cross-section points.  It does
        not specify the native spatial resolution of the 3DEP data.  If using this as a
        package the query_dems function in nldi-xstool.ancillary can be used to discover
        the available native resolution of the 3DEP data at the bounding box of the
        cross-section.

    Args:
        path (List[Tuple[float, float]]): List of tuples containing coordinate pairs
            of the end-points in order from river-left to river-right,
            for example: [(x1,y1), (x2,y2)]
        numpts (int): Number of points to interpolate along path.
        crs (Optional[str], optional): crs of input data. Defaults to "epsg:4326".
        file (Optional[str], optional): path/to/file.json. Defaults to None and returns
            a GeoDataFrame.
        res (Optional[int], optional): Spatial resolution of 3DEP Dem data. Defaults to
            10 which is available throughout CONUS.

    Returns:
        Union[int, gpd.GeoDataFrame]: If a file is specified it writes a json file and
            returns 0, otherwise it returns the cross-section in a GeoDataFrame.
    """
    lnst = []
    for pt in path:
        lnst.append(Point(pt[0], pt[1]))

    # print(ls1)
    d = {"name": ["xspath"], "geometry": [LineString(lnst)]}
    gpd_pth = gpd.GeoDataFrame(d, crs=crs)
    # print(gpd_pth)
    # gpd_pth.set_crs(epsg=4326, inplace=True)
    gpd_pth.to_crs(epsg=3857, inplace=True)
    # print(gpd_pth)
    xs = PathGen(path_geom=gpd_pth, ny=numpts)
    xs_line = xs.get_xs()
    # print(xs_line.head())
    # print(xs_line.total_bounds, xs_line.bounds)
    bb = xs_line.total_bounds - ((100.0, 100.0, -100.0, -100.0))
    # print('before dem', bb)
    dem = py3dep.get_map(
        "DEM", tuple(bb), resolution=res, geo_crs="EPSG:3857", crs="epsg:3857"
    )

    # print('after dem')
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=("z", x), y=("z", y))
    pdsi = dsi.to_dataframe()

    gpdsi = dataframe_to_geodataframe(pdsi, crs="epsg:3857")
    gpdsi["distance"] = _get_dist(gpdsi)
    gpdsi.to_crs(epsg=4326, inplace=True)
    if file:
        with open(file, "w") as f:
            f.write(gpdsi.to_json())
            f.close()
            return 0
    else:
        return gpdsi


def _get_dist(gdf: gpd.GeoDataFrame) -> Any:
    data = gdf.to_crs(epsg=5071)
    x1 = data["geometry"].x.values[0] - data["geometry"].x.values[:]
    y1 = data["geometry"].y.values[0] - data["geometry"].y.values[:]
    return np.hypot(x1, y1)


def _get_dist_path(gdf: gpd.GeoDataFrame) -> npt.NDArray[np.float64]:
    data = gdf.to_crs(epsg=5071)
    distance = []
    for index, g in enumerate(data.geometry):
        if index == 0:
            p1 = g
            p2 = g
            distance.append(0.0)
        else:
            p1 = p2
            p2 = g
            x1 = p2.x - p1.x
            y1 = p2.y - p1.y
            sumd = distance[-1]
            distance.append(sumd + np.hypot(x1, y1))
    return np.array(distance)


def getxsatpoint(
    point: List[float],
    numpoints: int,
    width: float,
    file: Optional[str] = None,
    res: Optional[int] = 10,
) -> Optional[Union[gpd.GeoDataFrame, None]]:
    """Get cross-section at nearest stream-segment and closest intersecton to point.

    Function uses the U.S. Geological Survey's NLDI to find the nearest NHD stream-
    segment, and generate a cross-section perpendicular to the nearest intersection
    of the point and stream-segment.

    Note 1:
        Cross-section is interpolated using 3DEP elevation services which does not
        include bathymetric data.

    Note 2:
        The parameter res specifices the spatial resolution of the 3DEP data that is
        interpolated to return elevation values of the cross-section points.  It does
        not specify the native spatial resolution of the 3DEP data.  If using this as a
        package the query_dems function in nldi-xstool.ancillary can be used to discover
        the available native resolution of the 3DEP data at the bounding box of the
        cross-section.

    Args:
        point (List[float]): Point of interest, for example [x,y]
        numpoints (int): Number of points to interpolate along path.
        width (float): Width of the cross-section centered on the stream-segment
        file (Optional[str], optional): path/to/file.json. Defaults to None and returns
            a GeoDataFrame.
        res (Optional[int], optional): Spatial resolution of 3DEP Dem data. Defaults to
            10 which is available throughout CONUS.

    Returns:
        Union[int, gpd.GeoDataFrame]: If a file is specified it writes a json file and
            returns 0, otherwise it returns the cross-section in a GeoDataFrame.
    """
    # print(file, type(file))
    # tpoint = f'POINT({point[1]} {point[0]})'
    df = pd.DataFrame(
        {"pointofinterest": ["this"], "Lat": [point[1]], "Lon": [point[0]]}
    )
    gpd_pt = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Lon, df.Lat))
    gpd_pt.set_crs(epsg=4326, inplace=True)
    gpd_pt.to_crs(epsg=3857, inplace=True)
    try:
        comid = __get_cid_from_lonlat(point)
    except Exception as ex:  # pragma: no cover
        # print(f'Error: {ex} unable to find comid - check lon lat coords')
        sys.exit(f"Error: {ex} unable to find comid - check lon lat coords")
    # print(f'comid = {comid}')
    strm_seg = NLDI().getfeature_byid("comid", comid).to_crs("epsg:3857")
    xs = XSGen(point=gpd_pt, cl_geom=strm_seg, ny=numpoints, width=width, tension=10.0)
    xs_line = xs.get_xs()
    # print(comid, xs_line)
    # get topo polygon with buffer to ensure there is enough topography to interpolate
    # xs line with coarsest DEM (30m) 100. m should
    bb = xs_line.total_bounds - ((100.0, 100.0, -100.0, -100.0))
    dem = py3dep.get_map(
        "DEM", tuple(bb), resolution=res, geo_crs="EPSG:3857", crs="epsg:3857"
    )
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=("z", x), y=("z", y))
    pdsi = dsi.to_dataframe()
    gpdsi = dataframe_to_geodataframe(pdsi, crs="epsg:3857")
    gpdsi["distance"] = _get_dist(gpdsi)
    gpdsi.to_crs(epsg=4326, inplace=True)
    if file:
        with open(str(file), "w") as f:
            f.write(gpdsi.to_json())
            f.close()
        return None
    else:
        return gpdsi  # pragma: no cover


def __lonlat_to_point(lon: float, lat: float) -> Point:  # noqa D103
    return Point(lon, lat)


def __get_cid_from_lonlat(point: List[float]) -> str:
    # print(point)
    pt = __lonlat_to_point(point[0], point[1])

    location = pt.wkt
    location = f"POINT({point[0]} {point[1]})"
    domain = "https://labs.waterdata.usgs.gov"
    path = "/api/nldi/linked-data/comid/position?f=json&coords="
    base_url = domain + path
    url = base_url + location
    # print(url)
    try:
        response = requests.get(url)
        # print(f'this is the response: {response}')
        response.raise_for_status()
        jres = response.json()
        comid = jres["features"][0]["properties"]["comid"]

    except requests.exceptions.RequestException as err:  # pragma: no cover
        print("OOps: Something Else", err)
    except requests.exceptions.HTTPError as errh:  # pragma: no cover
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:  # pragma: no cover
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:  # pragma: no cover
        print("Timeout Error:", errt)
    except Exception as ex:  # pragma: no cover
        raise ex

    return str(comid)
