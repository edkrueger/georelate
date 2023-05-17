"""Tests _distance.py"""

# pylint:disable=duplicate-code
import numpy as np
import pandas as pd
from georelate._distance import haversine, distance_table, design_matrix


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


def test_distance_table_with_defaults():
    """Tests the distance table function with defaults."""

    # austin
    austin_lat = [30.2672, 30.2673]
    austin_lon = [97.7431, 97.7432]

    # houston
    houston_lat = [29.7604, 29.7605, 29.7606]
    houston_lon = [95.3698, 95.3698, 95.3699]

    austin_df = pd.DataFrame(
        {
            "lat": austin_lat,
            "lon": austin_lon,
        }
    )

    houston_df = pd.DataFrame(
        {
            "lat": houston_lat,
            "lon": houston_lon,
        }
    )

    result_df = distance_table(left=austin_df, right=houston_df)

    assert result_df.shape[0] == austin_df.shape[0] * houston_df.shape[0]
    assert "distance" in result_df.columns
    assert result_df["distance"].dtype == np.float64
    assert {
        "lat_left",
        "lon_left",
        "lat_right",
        "lon_right",
        "index_left",
        "index_right",
    }.issubset(set(result_df.columns))

    print(result_df)
    print(result_df.dtypes)
    print(result_df["distance"].dtype)
    print(type(result_df["distance"].dtype))


def test_distance_table_some_options_1():
    """Tests the distance table function with some options."""

    # austin
    austin_id = [2, 5]
    austin_lat = [30.2672, 30.2673]
    austin_lon = [97.7431, 97.7432]

    # houston
    houston_id = [3, 6, 7]
    houston_lat = [29.7604, 29.7605, 29.7606]
    houston_lon = [95.3698, 95.3698, 95.3699]

    austin_df = pd.DataFrame(
        {
            "austin_lat": austin_lat,
            "austin_lon": austin_lon,
        },
        index=pd.Series(austin_id, name="austin_index"),
    )

    houston_df = pd.DataFrame(
        {
            "houston_lat": houston_lat,
            "houston_lon": houston_lon,
        },
        index=pd.Series(houston_id, name="houston_index"),
    )

    result_df = distance_table(
        left=austin_df,
        right=houston_df,
        left_lat="austin_lat",
        left_lon="austin_lon",
        right_lat="houston_lat",
        right_lon="houston_lon",
    )

    assert result_df.shape[0] == austin_df.shape[0] * houston_df.shape[0]
    assert "distance" in result_df.columns
    assert result_df["distance"].dtype == np.float64
    assert {
        "austin_lat",
        "austin_lon",
        "houston_lat",
        "houston_lon",
        "austin_index",
        "houston_index",
    }.issubset(set(result_df.columns))


def test_distance_table_some_options_2():
    """Tests the distance table function with some options."""

    # austin
    austin_id = [2, 5]
    austin_lat = [30.2672, 30.2673]
    austin_lon = [97.7431, 97.7432]

    # houston
    houston_id = [3, 6, 7]
    houston_lat = [29.7604, 29.7605, 29.7606]
    houston_lon = [95.3698, 95.3698, 95.3699]

    austin_df = pd.DataFrame(
        {"austin_lat": austin_lat, "austin_lon": austin_lon, "austin_id": austin_id},
    )

    houston_df = pd.DataFrame(
        {
            "houston_lat": houston_lat,
            "houston_lon": houston_lon,
            "houston_id": houston_id,
        },
    )

    result_df = distance_table(
        left=austin_df,
        right=houston_df,
        left_id="austin_id",
        right_id="houston_id",
        left_lat="austin_lat",
        left_lon="austin_lon",
        right_lat="houston_lat",
        right_lon="houston_lon",
    )

    assert result_df.shape[0] == austin_df.shape[0] * houston_df.shape[0]
    assert "distance" in result_df.columns
    assert result_df["distance"].dtype == np.float64
    assert {
        "austin_lat",
        "austin_lon",
        "houston_lat",
        "houston_lon",
        "austin_id",
        "houston_id",
    }.issubset(set(result_df.columns))


def test_distance_table_some_options_3():
    """Tests the distance table function with some options."""

    # austin
    austin_id = [2, 5]
    austin_lat = [30.2672, 30.2673]
    austin_lon = [97.7431, 97.7432]

    # houston
    houston_id = [3, 6, 7]
    houston_lat = [29.7604, 29.7605, 29.7606]
    houston_lon = [95.3698, 95.3698, 95.3699]

    austin_df = pd.DataFrame(
        {"lat": austin_lat, "lon": austin_lon, "id": austin_id},
    )

    houston_df = pd.DataFrame(
        {
            "lat": houston_lat,
            "lon": houston_lon,
            "id": houston_id,
        },
    )

    result_df = distance_table(
        left=austin_df,
        right=houston_df,
        left_id="id",
        right_id="id",
        left_lat="lat",
        left_lon="lon",
        right_lat="lat",
        right_lon="lon",
    )

    assert result_df.shape[0] == austin_df.shape[0] * houston_df.shape[0]
    assert "distance" in result_df.columns
    assert result_df["distance"].dtype == np.float64
    assert {
        "lat_left",
        "lon_left",
        "lat_right",
        "lon_right",
        "id_left",
        "id_right",
    }.issubset(set(result_df.columns))


def test_design_matrix_some_options_1():
    """Tests the design matrix function with some options."""

    k = 2

    # austin
    austin_id = [2, 5]
    austin_lat = [30.2672, 30.2673]
    austin_lon = [97.7431, 97.7432]

    # houston
    houston_id = [3, 6, 7]
    houston_lat = [29.7604, 29.7605, 29.7606]
    houston_lon = [95.3698, 95.3698, 95.3699]
    houston_other = [555, 666, 777]

    austin_df = pd.DataFrame(
        {
            "austin_lat": austin_lat,
            "austin_lon": austin_lon,
        },
        index=pd.Series(austin_id, name="austin_index"),
    )

    houston_df = pd.DataFrame(
        {
            "houston_lat": houston_lat,
            "houston_lon": houston_lon,
            "houston_other": houston_other,
        },
        index=pd.Series(houston_id, name="houston_index"),
    )

    result_df = distance_table(
        left=austin_df,
        right=houston_df,
        left_lat="austin_lat",
        left_lon="austin_lon",
        right_lat="houston_lat",
        right_lon="houston_lon",
    )

    result_df = design_matrix(
        left=austin_df,
        right=houston_df,
        left_lat="austin_lat",
        left_lon="austin_lon",
        right_lat="houston_lat",
        right_lon="houston_lon",
        k_closest=k,
    )

    print(result_df.T.to_string())

    assert result_df.shape[0] == austin_df.shape[0]

    excepted_columns = {"austin_index", "austin_lat", "austin_lon"}
    expected_closest_k_columns = {
        "houston_index",
        "houston_lat",
        "houston_lon",
        "houston_other",
        "distance",
    }
    all_expected_columns = excepted_columns | {
        f"{col}_{j+1}_closest" for col in expected_closest_k_columns for j in range(k)
    }

    assert all_expected_columns.issubset(set(result_df.columns))
