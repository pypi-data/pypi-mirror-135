# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_prometheus_sd',
 'netbox_prometheus_sd.api',
 'netbox_prometheus_sd.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netbox-plugin-prometheus-sd',
    'version': '0.3.0',
    'description': 'A Netbox plugin to provide Netbox entires to Prometheus HTTP service discovery',
    'long_description': "# netbox-plugin-prometheus-sd\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![CI](https://github.com/FlxPeters/netbox-plugin-prometheus-sd/workflows/CI/badge.svg?event=push)](https://github.com/FlxPeters/netbox-plugin-prometheus-sd/actions?query=workflow%3ACI)\n[![PyPI](https://img.shields.io/pypi/v/netbox-plugin-prometheus-sd)](https://pypi.org/project/netbox-plugin-prometheus-sd/)\n\nProvide Prometheus http_sd compatible API Endpoint with data from Netbox.\n\nHTTP SD is a new feature in Prometheus 2.28.0 that allows hosts to be found via a URL instead of just files. \nThis plugin implements API endpoints in Netbox to make devices, IPs and virtual machines available to Prometheus.\n\n## Installation\n\nThe plugin is available as a Python package in pypi and can be installed with pip\n\n    pip install netbox-plugin-prometheus-sd\n\nEnable the plugin in /opt/netbox/netbox/netbox/configuration.py:\n\n    PLUGINS = ['netbox_prometheus_sd']\n\nThe plugin has not further plugin configuration at the moment.\n\n## Usage\n\nThe plugin only provides a new API endpoint on the Netbox API. There is no further action required after installation. \n\n### API\n\nThe plugin reuses Netbox API view sets with new serializers for Prometheus. \nThis means that all filters that can be used on the Netbox api can also be used to filter Prometheus targets.\nPaging is disabled because Prometheus does not support paged results. \n\nThe plugin also reuses the Netbox authentication and permission model. \nDepending on the Netbox configuration, a token with valid object permissions must be passed to Netbox.\n\n```\nGET        /api/plugins/prometheus-sd/devices/              Get a list of devices in a prometheus compatible format\nGET        /api/plugins/prometheus-sd/virtual-machines/     Get a list of vms in a prometheus compatible format\nGET        /api/plugins/prometheus-sd/ip-addresses/         Get a list of ip in a prometheus compatible format\n```\n\n### Example\n\nA working example on how to use this plugin with Prometheus is located at the `example` folder. Netbox content is created by using Netbox docker initializers.\n\nThe demo data doesn't make sense, but they are good enough for demonstrating how to configure Prometheus and get demo data to Prometheus service discovery.\n\nGo to the `example` folder and run `docker-compose up`. Prometheus should get available on `http://localhost:9090`. Netbox content should then be available in the service discovery tab. \n\n## Development\n\nWe use Poetry for dependency management and invoke as task runner. \nAs Netbox plugins cannot be tested standalone, we need invoke to start all code embedded in Netbox Docker containers.\n\nAll code to run in docker is located under `development` which is also the starting point for VScode remote containers (not finished yet).\n\nTo start a virtual env managed by poetry run `poetry shell`. \n",
    'author': 'Felix Peters',
    'author_email': 'felix.peters@breuninger.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
