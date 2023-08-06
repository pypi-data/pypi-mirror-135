# zenodopy

![Tests](https://github.com/lgloege/zenodopy/actions/workflows/tests.yaml/badge.svg)
[![codecov](https://codecov.io/gh/lgloege/zenodopy/branch/main/graph/badge.svg?token=FVCS71HPHC)](https://codecov.io/gh/lgloege/zenodopy)
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/lgloege/zenodopy/issues)

A Python 3.6+ package to manage Zenodo repositories. 

Implemented functionality includes:
- `.create_project()`: create a new project
- `.upload_file()`: upload file to project
- `.download_file()`: download a file from a project
- `.delete_file()`: permanently removes a file from a project

Installing
----------

### GitHub
```sh
pip install -e git+https://github.com/lgloege/zenodopy.git#egg=zenodopy
```

### TestPyPi
```sh
pip install --extra-index-url https://test.pypi.org/simple/ zenodopy==0.1.0
```


Notes
----------
This project is under active development. Here is a list of things that needs improvement:
- **more tests**: need to test uploading and downloading files
- **documentation**: need to setup a readthedocs
- **download based on DOI**: right now you can only download from your own projects. Would be nice to download from 
- **asyncronous functions**: use `asyncio` and `aiohttp` to write async functions. This will speed up downloading multiple files. 
