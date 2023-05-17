"""Computes distances."""

# pylint:disable=too-many-arguments, too-many-locals
import numpy as np
import pandas as pd


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


def _get_id_keys(
    left,
    right,
    left_id,
    right_id,
):
    """_summary_

    Args:
        left (_type_): _description_
        right (_type_): _description_
        left_id (_type_): _description_
        right_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    left_index_name = left.index.name if left.index.name else "index"
    right_index_name = right.index.name if right.index.name else "index"

    left_id_key = left_id if left_id else left_index_name
    right_id_key = right_id if right_id else right_index_name

    return left_id_key, right_id_key


def _get_id_keys_with_potential_suffix(left, right, left_id, right_id, suffixes):
    """_summary_

    Args:
        left (_type_): _description_
        right (_type_): _description_
        left_id (_type_): _description_
        right_id (_type_): _description_
        suffixes (_type_): _description_

    Returns:
        _type_: _description_
    """

    left_id_key, right_id_key = _get_id_keys(
        left=left,
        right=right,
        left_id=left_id,
        right_id=right_id,
    )

    if left_id_key == right_id_key:
        left_suffix, right_suffix = suffixes
        if left_suffix:
            left_id_key = f"{left_id_key}{left_suffix}"
        if right_suffix:
            right_id_key = f"{right_id_key}{right_suffix}"

    return left_id_key, right_id_key


def distance_table(
    left,
    right,
    left_id=None,
    right_id=None,
    left_lat="lat",
    left_lon="lon",
    right_lat="lat",
    right_lon="lon",
    suffixes=("_left", "_right"),
):
    """_summary_

    Args:
        left (DataFrame): Left DataFrame to merge with. Assumes the index is an id.
        right (DataFrame): Right DataFrame to merge with. Assumes the index is an id.
        left_id (str, optional): Column containing the id for the left DataFrame.
            If None is passed, assumes the index is the id.
            Defaults to None.
        right_id (str, optional): Column containing the id for the right DataFrame.
            If None is passed, assumes the index is the id.
            Defaults to None.
        left_lat (str, optional): Column containing the latitude in the left DataFrame.
            Defaults to "lat".
        left_lon (str, optional): Column containing the longitude in the left DataFrame.
            Defaults to "lon".
        right_lat (str, optional): Column containing the latitude in the right DataFrame.
            Defaults to "lat".
        right_lon (str, optional): Column containing the longitude in the right DataFrame.
            Defaults to "lon".
        suffixes (tuple, optional): A length-2 sequence where each element is optionally a string
            indicating the suffix to add to overlapping column names in left and right respectively.
            Pass a value of None instead of a string to indicate that the column name from
            left or right should be left as-is, with no suffix.
            At least one of the values must not be None.
            Defaults to ("_left", "_right").

    Returns:
        _type_: _description_
    """

    left_id_key, right_id_key = _get_id_keys(
        left=left,
        right=right,
        left_id=left_id,
        right_id=right_id,
    )

    merged_df = pd.merge(
        left=left.reset_index().loc[:, [left_id_key, left_lat, left_lon]],
        right=right.reset_index().loc[:, [right_id_key, right_lat, right_lon]],
        how="cross",
        suffixes=suffixes,
    )

    left_lat_key = (
        left_lat if left_lat in merged_df.columns else f"{left_lat}{suffixes[0]}"
    )
    left_lon_key = (
        left_lon if left_lon in merged_df.columns else f"{left_lon}{suffixes[0]}"
    )
    right_lat_key = (
        right_lat if right_lat in merged_df.columns else f"{right_lat}{suffixes[1]}"
    )
    right_lon_key = (
        right_lon if right_lon in merged_df.columns else f"{right_lon}{suffixes[1]}"
    )

    return merged_df.assign(
        distance=lambda df_: haversine(
            p1_lat=df_[left_lat_key],
            p1_lon=df_[left_lon_key],
            p2_lat=df_[right_lat_key],
            p2_lon=df_[right_lon_key],
        )
    )


def _k_closest(df, left_id, right_id, k):
    grouped = df.groupby(left_id)

    join_data = []

    for left_id_, group_df in grouped:
        design_row = {}

        nsmallest_df = group_df.nsmallest(n=k, columns="distance")

        design_row[left_id] = left_id_

        for idx, (_, row) in enumerate(nsmallest_df.iterrows()):
            design_row[f"{right_id}_{idx + 1 }_closest"] = row[right_id]
            design_row[f"distance_{idx + 1}_closest"] = row["distance"]

        join_data.append(design_row)

    return pd.DataFrame(join_data)


def design_matrix(
    left,
    right,
    left_id=None,
    right_id=None,
    left_lat="lat",
    left_lon="lon",
    right_lat="lat",
    right_lon="lon",
    suffixes=("_left", "_right"),
    k_closest=None,
):

    """_summary_

    Args:
        left (DataFrame): Left DataFrame to merge with. Assumes the index is an id.
        right (DataFrame): Right DataFrame to merge with. Assumes the index is an id.
        left_id (str, optional): Column containing the id for the left DataFrame.
            If None is passed, assumes the index is the id.
            Defaults to None.
        right_id (str, optional): Column containing the id for the right DataFrame.
            If None is passed, assumes the index is the id.
            Defaults to None.
        left_lat (str, optional): Column containing the latitude in the left DataFrame.
            Defaults to "lat".
        left_lon (str, optional): Column containing the longitude in the left DataFrame.
            Defaults to "lon".
        right_lat (str, optional): Column containing the latitude in the right DataFrame.
            Defaults to "lat".
        right_lon (str, optional): Column containing the longitude in the right DataFrame.
            Defaults to "lon".
        suffixes (tuple, optional): A length-2 sequence where each element is optionally a string
            indicating the suffix to add to overlapping column names in left and right respectively.
            Pass a value of None instead of a string to indicate that the column name from
            left or right should be left as-is, with no suffix.
            At least one of the values must not be None.
            Defaults to ("_left", "_right").
        k_closest (int, optional): Specifies the number of nearest observations
            for the right DataFrame to include in the output DataFrame
            for each observations in the left DataFrame.

    Returns:
        DataFrame: The design matrix.
    """

    left_id_key, right_id_key = _get_id_keys(
        left=left, right=right, left_id=left_id, right_id=right_id
    )

    left_id_key_w_suffix, right_id_key_w_suffix = _get_id_keys_with_potential_suffix(
        left=left, right=right, left_id=left_id, right_id=right_id, suffixes=suffixes
    )

    distance_df = distance_table(
        left,
        right,
        left_id=left_id,
        right_id=right_id,
        left_lat=left_lat,
        left_lon=left_lon,
        right_lat=right_lat,
        right_lon=right_lon,
        suffixes=suffixes,
    )

    left_df = left.reset_index()
    right_df = right.reset_index()

    k_closest_join_df = _k_closest(
        df=distance_df,
        left_id=left_id_key_w_suffix,
        right_id=right_id_key_w_suffix,
        k=k_closest,
    )

    out_df = left_df.copy()

    if k_closest:
        k_closest_join_df = _k_closest(
            df=distance_df,
            left_id=left_id_key_w_suffix,
            right_id=right_id_key_w_suffix,
            k=k_closest,
        )
        assert set(k_closest_join_df[left_id_key_w_suffix].values) == set(
            left_df[left_id_key].values
        )
        out_df = pd.merge(
            out_df,
            k_closest_join_df,
            left_on=left_id_key,
            right_on=left_id_key_w_suffix,
        )

        for j in range(k_closest):
            # pylint:disable=cell-var-from-loop
            right_k_df = right_df.rename(columns=lambda col: f"{col}_{j + 1}_closest")
            out_df = pd.merge(
                out_df,
                right_k_df,
                left_on=f"{right_id_key_w_suffix}_{j + 1}_closest",
                right_on=f"{right_id_key}_{j + 1}_closest",
            )

    return out_df
