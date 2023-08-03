"""Code for example currently in README.md"""

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

print(left_df.to_html())
print(right_df.to_html())
print(df.to_html())

print(df.columns)
