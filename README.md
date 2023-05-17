# georelate
Georelate constructs design matrices from geographical data.

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