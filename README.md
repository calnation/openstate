openstate
--------
Generates CSV files for use in a wiki.

## Install

### pip install from github repository.

```sh
$ pip install git+https://github.com/calnation/openstate
$ openstate
```

## Use
Add a `openstate.ini` file to `/` directory and include in it the following:
```sh
[main]
OPENSTATES_API_KEY = 
OUTPUT_PATH = 
STATE = 
TZ = 
```

To use (with caution), simply:

```sh
$ openstate schedule all
```
