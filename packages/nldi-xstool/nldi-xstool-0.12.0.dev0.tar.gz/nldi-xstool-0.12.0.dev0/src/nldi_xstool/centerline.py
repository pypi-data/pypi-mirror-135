"""Centerline."""
from typing import Any
from typing import Tuple

import geopandas as gpd
import numpy as np
import numpy.typing as npt

from .tspline import tspline


class Centerline:
    """Centerline.

    class to take a centerline as a shapefile and create a tension spline to be used
    with inherited class curvilinear grid
    """

    def __init__(
        self: "Centerline", center_shp: gpd.GeoDataFrame, nx: int, tension: float
    ) -> None:
        """Init Centerline class.

        Args:
            center_shp (gpd.GeoDataFrame): centerline shape
            nx (int): Number of interpolatin points.
            tension (float): Centerline tension-spline interpolation tension (.1 - 100.)
        """
        self.center_shp = center_shp
        self.gpdata = center_shp
        self.x = np.empty(0, dtype=np.double)
        self.y = np.empty(0, dtype=np.double)
        self.tension = tension
        self.numclpts = 0
        self.numInterpPts = nx
        self.si = np.empty(0, dtype=np.double)
        self.temp = np.empty(0, dtype=np.double)
        self.yp = np.empty(0, dtype=np.double)
        self.xo_interp = np.empty(0, dtype=np.double)
        self.yo_interp = np.empty(0, dtype=np.double)
        self.phi_interp = np.empty(0, dtype=np.double)
        self.r_interp = np.empty(0, dtype=np.double)
        self.stot = np.empty(0, dtype=np.double)
        self.sout = np.empty(0, dtype=np.double)
        self.__initialize()
        self.__getspline(nx, self.tension)

    def __initialize(self: "Centerline") -> None:
        tx = []
        ty = []
        for _index, row in self.gpdata.iterrows():
            for pt in list(row["geometry"].coords):
                # print(pt, type(pt))
                tx.append(pt[0])
                ty.append(pt[1])
        self.x = np.array(tx)
        self.y = np.array(ty)
        self.numclpts = self.x.size
        print(self.numclpts)

    # def description(self):
    #     return "{} used the shapfile {}".format("centerline", self.center_shp)

    # def getCLShapeFile(self):
    #     return self.center_shp

    # def getlength(self): #
    #     return

    def getpoints(
        self: "Centerline",
    ) -> Tuple[npt.NDArray[np.double], npt.NDArray[np.double]]:
        """Get centerline points.

        Returns:
            [type]: [description]
        """
        return self.x, self.y

    def getinterppts(self) -> Tuple[npt.NDArray[np.double], npt.NDArray[np.double]]:
        """Get interpolated centerline points."""
        return self.xo_interp, self.yo_interp

    def getinterppts_dyn(
        self: "Centerline", numinterppts: int, tension: float
    ) -> Tuple[npt.NDArray[np.double], npt.NDArray[np.double]]:
        """Get interpolated centerline points when user moving points interactively.

        Args:
            numinterppts (int): [description]
            tension (float): [description]

        Returns:
            [type]: [description]
        """
        print(tension)
        self.__getspline(numinterppts, tension)
        return self.xo_interp, self.yo_interp

    def getphiinterp(self: "Centerline", index: int) -> Any:  # noqa D102
        return self.phi_interp[index]

    def __getspline(self: "Centerline", numinterppts: int, tension: float) -> None:
        self.numInterpPts = numinterppts
        self.tension = tension
        self.xo_interp = np.zeros(self.numInterpPts)
        self.yo_interp = np.zeros(self.numInterpPts)
        self.phi_interp = np.zeros(self.numInterpPts)
        self.r_interp = np.zeros(self.numInterpPts)
        self.stot = np.zeros(self.numInterpPts)
        self.sout = np.zeros(self.numInterpPts)

        self.si = np.zeros(self.numclpts)
        self.temp = np.zeros(self.numclpts)
        self.yp = np.zeros(self.numclpts)

        for i in range(0, self.numclpts):
            if i == 0:
                self.si[i] = 0.0
            else:
                ds = np.power(
                    (
                        np.power((self.x[i] - self.x[i - 1]), 2)
                        + np.power((self.y[i] - self.y[i - 1]), 2)
                    ),
                    0.5,
                )
                self.si[i] = self.si[i - 1] + ds

        self.stot = self.si[self.numclpts - 1]
        for i in range(0, self.numInterpPts):
            self.sout[i] = i * self.stot / (self.numInterpPts - 1)
            # if i == 0:
            #     nsInc = self.stot / (self.numInterpPts - 1)
        if self.numclpts < 3:
            self.yp = np.zeros(3)
            self.temp = np.zeros(3)
            sitmp = np.zeros(3)
            sitmp = np.append(sitmp, [self.si[0]])
            sitmp = np.append(sitmp, [self.si[1] / 2])
            sitmp = np.append(sitmp, self.si[1])

            txctmp = np.zeros(3)
            txctmp = np.append(txctmp, self.x[0])
            txctmp = np.append(txctmp, self.x[0] + (self.x[1] - self.x[0]) / 2.0)
            txctmp = np.append(txctmp, self.x[1])

            tyctmp = np.zeros(3)
            tyctmp = np.append(tyctmp, self.y[0])
            tyctmp = np.append(tyctmp, self.y[0] + (self.y[1] - self.y[0]) / 2.0)
            tyctmp = np.append(tyctmp, self.y[1])

            tspline(
                sitmp,
                txctmp,
                3,
                self.sout,
                self.xo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
            tspline(
                sitmp,
                tyctmp,
                3,
                self.sout,
                self.yo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
        else:
            tspline(
                self.si,
                self.x,
                self.numclpts,
                self.sout,
                self.xo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
            tspline(
                self.si,
                self.y,
                self.numclpts,
                self.sout,
                self.yo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
        self.__calc_curvature()

    def __calc_curvature(self: "Centerline") -> None:
        for i in range(1, self.numInterpPts):
            dx = self.xo_interp[i] - self.xo_interp[i - 1]
            dy = self.yo_interp[i] - self.yo_interp[i - 1]
            if dx == 0.0:
                if dy > 0.0:
                    self.phi_interp[i] = np.pi / 2.0
                elif dy < 0.0:
                    self.phi_interp[i] = -1.0 * np.pi / 2.0
            else:
                self.phi_interp[i] = np.arctan2(dy, dx)
        self.phi_interp[0] = (2.0 * self.phi_interp[1]) - self.phi_interp[2]
        scals = np.float64(self.stot / (self.numInterpPts - 1))
        for i in range(1, self.numInterpPts):
            dx = self.xo_interp[i] - self.xo_interp[i - 1]
            dphi = np.fabs(self.phi_interp[i]) - np.fabs(self.phi_interp[i - 1])
            if dphi <= 0.0001:
                self.r_interp[i] = 100000000.0
            else:
                self.r_interp[i] = scals / dphi
