"""Computes distances."""

import numpy as np


def haversine(p1_lat, p1_lon, p2_lat, p2_lon, radius=6367):
    """Computes the distances between 2 list of points of the same length.

    Note: The Earth is not perfectly spherical, so there isn't one right number for the radius.

    Args:
        p1_lat (ArrayLike[Number]): An array of latitudes form the first list of coordinates.
        p1_lon (ArrayLike[Number]): An array of longitudes form the first list of coordinates.
        p2_lat (ArrayLike[Number]): An array of latitudes form the second list of coordinates.
        p2_lon (ArrayLike[Number]): An array of longitudes form the second list of coordinates.
        radius (int, optional): Radius of the Earth. Defaults to 6367.

    Returns:
        ArrayLike[Number]: An array of distances between the points in kms.
    """

    p1_lon_r, p1_lat_r, p2_lon_r, p2_lat_r = map(
        np.radians, [p1_lon, p1_lat, p2_lon, p2_lat]
    )

    d_lon_r = p2_lon_r - p1_lon_r
    d_lat_r = p2_lat_r - p1_lat_r

    partial = (
        np.sin(d_lat_r / 2) ** 2
        + np.cos(p1_lat_r) * np.cos(p2_lat_r) * np.sin(d_lon_r / 2) ** 2
    )
    d_r = 2 * np.arcsin(np.sqrt(partial))

    return radius * d_r
