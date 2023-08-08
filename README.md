# GEORELATE
Georelate constructs design matrices from geographical data.

## User Guide

### Description

GEORELATE can take any 2 datasets, each containing a set of geographic points, and output a new dataset that includes variables indicating which points in one dataset are closest to each point in the other. GEORELATE also creates a new set of variables in the output dataset that indicate how far apart each point is from the nearest points in the other dataset.   

### Installation

GEORELATE can be installed by running the line below:  

`pip install georelate`

Requirements:  
Python 3.10+  

### GEORELATE in action
To more clearly demonstrate GEORELATE’s functionality in the sections below we include an example of how to apply the package with sample files and code.  

The two input files below contain fictionalized data for Brazil. The first contains the IDs and geographic coordinates of polling stations. The second contains the same information for new foreign aid projects. The image below that shows the two sets of points overlayed on a map of Brazil. Finally, GEORELATE was used to create the output dataset shown below the map. The output dataset contains the IDs and distances away of the 3 closest aid projects to each polling station. 

**The input and out files are below:**

**Polling Stations**

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>local_id</th>
      <th>lat</th>
      <th>lon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>-6.69255</td>
      <td>-39.76566</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>-4.76871</td>
      <td>-39.61186</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>-3.28926</td>
      <td>-40.75443</td>
    </tr>
  </tbody>
</table>

**Aid Projects**
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>project_id_aid</th>
      <th>lat_aid</th>
      <th>long_aid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>p1</td>
      <td>-6.61616</td>
      <td>-39.97990</td>
    </tr>
    <tr>
      <th>1</th>
      <td>p2</td>
      <td>-4.76871</td>
      <td>-39.77116</td>
    </tr>
    <tr>
      <th>2</th>
      <td>p3</td>
      <td>-4.26065</td>
      <td>-39.39030</td>
    </tr>
  </tbody>
</table>


**Map**

Blue = polling stations

Red = aid projects

![Capture 500 w](https://github.com/edkrueger/georelate/assets/7817442/1caf5761-9392-4a72-8380-c4f58d89e5ef)

![Plot](/docs/artifacts/plot.png)

**Output** 
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>local_id</th>
      <th>project_id_aid_1_closest</th>
      <th>distance_1_closest</th>
      <th>project_id_aid_2_closest</th>
      <th>distance_2_closest</th>
      <th>project_id_aid_3_closest</th>
      <th>distance_3_closest</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>p1</td>
      <td>25.124568</td>
      <td>p2</td>
      <td>213.787803</td>
      <td>p3</td>
      <td>273.415835</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>p3</td>
      <td>185.826237</td>
      <td>p2</td>
      <td>197.251459</td>
      <td>p1</td>
      <td>379.513297</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>p2</td>
      <td>17.640953</td>
      <td>p3</td>
      <td>61.562643</td>
      <td>p1</td>
      <td>209.292590</td>
    </tr>
  </tbody>
</table>


#### Example Code
Below I include the code used to create the output file (output.csv).

```python
from georelate import design_matrix
from georelate.data import load_poll_aid_data

# load in the foreign_aid data and the polling station data 
left_df, right_df = load_poll_aid_data()

# the code below creates the output dataset
df = design_matrix(
  left = left_df, 
  right = right_df, 
  left_id = "local_id", 
  right_id = "project_id_aid", 
  right_lat = "lat_aid", 
  right_lon = "long_aid", 
  k_closest=3
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
