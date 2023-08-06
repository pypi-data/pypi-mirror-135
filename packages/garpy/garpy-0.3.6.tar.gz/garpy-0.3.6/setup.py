# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['garpy']

package_data = \
{'': ['*'], 'garpy': ['resources/*']}

install_requires = \
['PyYAML>=5.1,<7.0',
 'attrs>=21.4.0,<22.0.0',
 'click>=7,<9',
 'cloudscraper>=1.2.58,<2.0.0',
 'pendulum>=2.0,<3.0',
 'requests>=2.22,<3.0',
 'tqdm>=4.36,<5.0']

entry_points = \
{'console_scripts': ['garpy = garpy.cli:main']}

setup_kwargs = {
    'name': 'garpy',
    'version': '0.3.6',
    'description': 'Python client for downloading activities from Garmin Connect',
    'long_description': '###################################\nGarpy: Make your garmin data yours!\n###################################\n\n|PyPI-Versions| |PyPI-Status| |Codacy-Grade| |Tests| |Coveralls|\n\n``garpy`` is a simple app used to backup your data from Garmin Connect. It can be used to do incremental\nbackups of your data from Garmin Connect or to download one specific activity.\n\n********************************\nIncremental backup of activities\n********************************\n\nThe first time you use it, all the activities found on your Garmin Connect account will be downloaded to\nthe directory that you specify. Afterwards, each time you run the command, only the newly available\nactivities will be downloaded.\n\nThe command is used as follows:\n\n.. code:: sh\n\n    garpy download {backup-dir}\n\nBehind the scenes, this is what will happen:\n\n- `garpy` will prompt you for your password and will then authenticate against Garmin Connect.\n- It will first fetch the list of all your activities from garmin.\n- It will check which activities have already been backed up on the given `backup-dir`\n- It will proceed to download all the missing activities.\n\n************************************\nDownloading one activity from its ID\n************************************\n\nIf you wish to download only one activity or simple you want to refresh an already downloaded activity,\nuse the \'-a/--activity\' flag as follows:\n\n.. code:: sh\n\n    garpy download --activity 1674567326 {backup-dir}\n\nThis will download the activity in all existing formats to the given `backup_dir`\n\n****************\nFull CLI options\n****************\n\nFor more detailed usage, invoke the \'--help\' command:\n\n.. code:: sh\n\n    $ garpy download --help\n    Usage: garpy download [OPTIONS] [BACKUP_DIR]\n\n      Download activities from Garmin Connect\n\n      Entry point for downloading activities from Garmin Connect. By default, it\n      downloads all newly created activities since the last time you did a\n      backup.\n\n      If you specify an activity ID with the "-a/--activity" flag, only that\n      activity will be downloaded, even if it has already been downloaded\n      before.\n\n      If no format is specified, the app will download all possible formats.\n      Otherwise you can specify the formats you wish to download with the\n      "-f/--formats" flag. The flag can be used several  times if you wish to\n      specify several formats, e.g., \'garpy download [OPTIONS] -f original -f\n      gpx [BACKUP_DIR]\' will download .fit and .gpx files\n\n    Options:\n      -f, --formats [tcx|gpx|original|summary|fit|details]\n                                      Which formats to download. The flag can be\n                                      used several times, e.g. \'-f original -f\n                                      gpx\'\n      -u, --username {username}       Username of your Garmin account\n      -p, --password {password}       Password of your Garmin account\n      -a, --activity {ID}             Activity ID. If indicated, download only\n                                      that activity, even if it has already been\n                                      downloaded. Otherwise, do incremental update\n                                      of backup\n      --help                          Show this message and exit.\n\n\n************\nInstallation\n************\n``garpy`` requires Python 3.6 or higher on your system. For those who know your way around with Python, install\n``garpy`` with pip as follows:\n\n.. code:: sh\n\n    pip install -U garpy\n\n\nIf you are new to Python or have Python 2 installed on your\ncomputer, I recommend you install Miniconda_. To my knowledge, it is the simplest way of installing a robust and\nlightweight Python environment.\n\n\n****************\nAcknowledgements\n****************\n\nThe library is based on garminexport_. I borrowed the GarminClient, refactored it to my taste and\ncreated a package from it.\n\n\n.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/garpy.svg?logo=python&logoColor=white\n   :target: https://pypi.org/project/garpy\n.. |PyPI-Status| image:: https://img.shields.io/pypi/v/garpy.svg\n   :target: https://pypi.org/project/garpy\n.. |Codacy-Grade| image:: https://api.codacy.com/project/badge/Grade/2fbbd268e0a04cd0983291227be53873\n   :target: https://app.codacy.com/manual/garpy/garpy/dashboard\n.. |Tests| image:: https://github.com/felipeam86/garpy/actions/workflows/test.yml/badge.svg\n    :target: https://github.com/felipeam86/garpy/actions/workflows/test.yml\n.. |Coveralls| image:: https://coveralls.io/repos/github/felipeam86/garpy/badge.svg?branch=develop\n    :target: https://coveralls.io/github/felipeam86/garpy?branch=develop\n\n\n.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html\n.. _garminexport: https://github.com/petergardfjall/garminexport\n',
    'author': 'Felipe Aguirre Martinez',
    'author_email': 'felipeam86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felipeam86/garpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.15,<4.0.0',
}


setup(**setup_kwargs)
