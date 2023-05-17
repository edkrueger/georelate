"""Tests _distance.py"""

# pylint:disable=duplicate-code
from georelate._distance import haversine


def test_haversine():
    """Tests the haversine function."""

    # austin
    p1_lat = [30.2672]
    p1_lon = [97.7431]

    # houston
    p2_lat = [29.7604]
    p2_lon = [95.3698]

    # in km, rounded to nearest int
    distance = [235]

    result = haversine(p1_lat=p1_lat, p1_lon=p1_lon, p2_lat=p2_lat, p2_lon=p2_lon)

    assert result.round(0) == [distance]
