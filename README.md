# georelate
Georelate constructs design matrices from geographical data.

## User Guide

### Description

GEORELATE can take any 2 datasets, each containing a set of geographic points, and outputs a new dataset that includes variables indicating which points in one dataset are closest to each point in the other. GEORELATE also creates a new set of variables in the output dataset that indicate how far apart each point is from the nearest points in the other dataset.   

### Installation

GEORELATE can be installed by running the line below:  

`pip install georelate`

Requirements:  
Python 3.10+  

### GEORELATE in action
To more clearly demonstrate GEORELATE’s functionality in the sections below I include an example of how to apply the package with sample files and code.  
The two input files below contain fictionalized data for Brazil. The first (polling_stations.csv) contains the IDs and geographic coordinates of polling stations. The second (foreign_aid.csv) contains the IDs and geographic coordinates of new foreign aid projects. GEORELATE was used to create the output dataset (output.csv) below. The output dataset contains the IDs and distances away of the 2 closest aid projects to each polling station. 

#### Example Code
Below I include the code used to create the output file (output.csv).

```python
import pandas as pd
from georelate._distance import design_matrix

# Load in the foreign_aid data
left_df = pd.read.csv("foreign_aid")
# Load in the polling station data 
right_df = pd.read("polling_stations.csv")

# The code below creates the output dataset
design_matrix(
  left = left_df, 
  right = right_df, 
  left_id = "local_id", 
  right_id = "project_id_aid", 
  right_lat = "lat_aid", 
  right_lon = "long_aid", 
  k_closest=3)
)
```

A closer look at the code above...  
The line above that begins with “design_matrix” creates the final output file and includes 7 arguments.  
The first argument  (left = left_df) specifies the foreign aid projects dataset. GEORELATE will review all the coordinate points in this dataset to identify which foreign aid projects are nearest to the polling stations in the dataset specified in the second argument.  
The second argument (right = right_df) specifies the polling station dataset.  
The third argument (left_id = "local_id") specifies the column name containing the IDs of the foreign aid projects.  
The fourth argument (right_id = "project_id_aid") contains the column name containing the IDs of the polling stations.  
The fifth argument contains the column name containing the latitude of the foreign aid projects.  
The sixth argument contains the column name containing the longitude of the foreign aid projects.  
The last argument is used to set the number of nearest foreign projects GEORELATE will include in the final output file. In the example above it is set to 3. Therefore, the output file includes information about the 3 nearest foreign aid projects to each polling station.  



## Development

### Local Dev Instructions
Run `poetry install` to install the env.  
Run `poetry run pre-commit install` to initialize the git hooks.  
Run `poetry run pre-commit run --all-files` if there are file that were committed before adding the git hooks.  
Activate the shell with: `poetry shell`  
Lint with: `poetry run pylint georelate/ tests/`  
Test with: `poetry run pytest --cov=georelate`


### Pushing to PyPI

#### Environmental variables
Environmental variables are a good way to keep our tokens secret and our options configurable. To set them, copy `sample.envrc` to `.envrc` and change the values. Leave `PYPI_USERNAME=__token__` and change the value of `PYPI_PASSWORD` to your password.  
To load `.envrc`, one could just run `.envrc` as a shell script, but direnv will make things easier by automatically loading the variable when you enter the directory, once allowed.  
To install direnv on a mac running zsh, use brew to install with `brew install direnv` and hook in into your shell by adding `eval "$(direnv hook zsh)"` to your `.zshrc` file. For other install instructions see: https://direnv.net/.  
To allow direnv to load `.envrc` in a directory run `direnv allow`.  

Alternatively, set the values of the environmental variable using `export PYPI_USERNAME=__token__ && export PYPI_PASSWORD=<your-pypi-token>`

#### Push to PyPI
Run `poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD` to build and push the package to PyPI.
