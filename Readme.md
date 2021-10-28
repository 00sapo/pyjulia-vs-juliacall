# `pyjulia` vs `juliacall`

1. install poetry
2. `poetry install --no-root`
3. `poetry run python setup.py`
4. pyjulia: `poetry run python test.py pyjulia 8`
5. juliacall: `poetry run python test.py juliacall 8`
6. numba: `poetry run python test.py numba 8`
7. pure-python: `poetry run python test.py python 8`

## Results

### `N_JOBS = 8`
* `pyjulia`: 47.5 s
* `juliacall`: 83.4 s
* `numba`: 61.3 s
* `python`: > 300 s

### `N_JOBS = 1`
* `pyjulia`: 79.4 s
* `juliacall`: 86.3 s
* `numba`: 177.6 s
* `python`:  > 300 s
