# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sport_activities_features',
 'sport_activities_features.interruptions',
 'sport_activities_features.tests',
 'sport_activities_features.weather_objects']

package_data = \
{'': ['*'], 'sport_activities_features.tests': ['data/*']}

install_requires = \
['dotmap>=1.3.25,<2.0.0',
 'geopy>=2.0.0,<3.0.0',
 'geotiler>=0.14.5,<0.15.0',
 'gpxpy>=1.4.2,<2.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'niaaml>=1.1.6,<2.0.0',
 'overpy>=0.6,<0.7',
 'requests>=2.25.1,<3.0.0',
 'tcxreader>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'sport-activities-features',
    'version': '0.2.11',
    'description': 'A minimalistic toolbox for extracting features from sport activity files',
    'long_description': None,
    'author': 'iztokf',
    'author_email': 'iztokf@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
