"""Code for example currently in README.md"""

### include in code snippet

from georelate import design_matrix
from georelate.data import load_poll_aid_data

# load in the foreign_aid data and the polling station data
left_df, right_df = load_poll_aid_data()

# the code below creates the output dataset
df = design_matrix(
    left=left_df,
    right=right_df,
    left_id="local_id",
    right_id="project_id_aid",
    right_lat="lat_aid",
    right_lon="long_aid",
    k_closest=3,
)

### don't include in code snippet

if __name__ == "__main__":
    import os

    import geopandas as gpd
    from geodatasets import get_path
    import matplotlib.pyplot as plt

    world_gdp = gpd.read_file(get_path("naturalearth.land"))

    left_gdf = gpd.GeoDataFrame(
        left_df,
        geometry=gpd.points_from_xy(left_df["lon"], left_df["lat"]),
        crs="EPSG:4326",
    )

    right_gdf = gpd.GeoDataFrame(
        right_df,
        geometry=gpd.points_from_xy(right_df["long_aid"], right_df["lat_aid"]),
        crs="EPSG:4326",
    )

    ax = world_gdp.clip([-45, -8, -25, 15]).plot(color="white", edgecolor="black")
    left_gdf.plot(ax=ax, color="blue")
    right_gdf.plot(ax=ax, color="red")

    for x, y, label in zip(
        left_gdf.geometry.x, left_gdf.geometry.y, left_gdf["local_id"]
    ):
        ax.annotate(
            label,
            xy=(x, y),
            xytext=(20, 3),
            textcoords="offset points",
            arrowprops=dict(color="blue", headwidth=2, shrink=0.3),
            color="blue",
        )

    for x, y, label in zip(
        right_gdf.geometry.x, right_gdf.geometry.y, right_gdf["project_id_aid"]
    ):
        ax.annotate(
            label,
            xy=(x, y),
            xytext=(-30, -10),
            textcoords="offset points",
            arrowprops=dict(color="red", headwidth=2, shrink=0.3),
            color="red",
        )

    os.makedirs("docs/artifacts", exist_ok=True)
    plt.savefig("docs/artifacts/plot.png")

    # print(left_df.to_html())
    # print(right_df.to_html())
    # print(df.to_html())
    # print(df.columns)

    print(left_df)
    print(right_df)
    print(df)
    print(df.columns)
