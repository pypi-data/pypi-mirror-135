# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ngsildclient',
 'ngsildclient.api',
 'ngsildclient.model',
 'ngsildclient.model.helper',
 'ngsildclient.playground',
 'ngsildclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['geojson>=2.5.0,<3.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'ngsildclient',
    'version': '0.1.1',
    'description': 'ngsildclient is a Python library that helps building NGSI-LD entities and interacting with a NGSI-LD Context Broker.',
    'long_description': '# The ngsildclient library\n\n## Overview\n\n **ngsildclient** is a Python library that helps building NGSI-LD entities and interacting with a NGSI-LD Context Broker.\n\n While the library primary purpose is to **ease and speed up the development of a NGSI Agent**, it\'s also **valuable for Data Modeling in the design stage** especially in interactive mode *with the help of autocompletion* - such as in Python console or in Jupyter notebook.\n\n## Key Features\n\n### Build NGSI-LD entities\n\nThe task of building a large NGSI-LD compliant entity is tedious, error-prone and results in a significant amount of code. \n\nBy providing primitives to add properties and metadata in respect with the ETSI specification **ngsildclient** allows to build and manipulate NGSI-LD compliant entities without effort.\n\n### Implement the NGSI-LD API\n\n**ngsildclient** provides a NGSI-LD API Client implementation.\n\nActing as a Context Producer/Consumer **ngsildclient** is able to send/receive NGSI-LD entities to/from the Context Broker for creation and other operations.\n\nAs of v.01 it covers a subset of the API that consists of the ``/entities/{entityId}`` endpoint.\n\n## Smart Building Demo\n\nHow to build the NGSI-LD [example](https://smart-data-models.github.io/dataModel.Building/Building/examples/example-normalized.jsonld) from the [Smart Data Models Initiative](https://smartdatamodels.org/), and ask the Context Broker to create it.\n\n[![demo](https://asciinema.org/a/r328sRBCoKiDHuJHiBXNnQxqF.svg)](https://asciinema.org/a/r328sRBCoKiDHuJHiBXNnQxqF?autoplay=1&theme=solarized-dark&speed=3)\n\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at :\nhttps://github.com/Orange-OpenSource/python-orion-client\n\nBinary installer for the latest released version is available at the [Python\npackage index](https://pypi.org/project/ngsildclient).\n\n```sh\npip install ngsildclient\n```\n\n## Installation\n\n**ngsildclient** requires Python 3.9+.\n\nOne should use a virtual environment. For example with pyenv.\n\n```sh\nmkdir myfiwareproject && cd myfiwareproject\npyenv virtualenv 3.10.1 myfiwareproject\npyenv local\npip install ngsildclient\n```\n\n## Getting started\n\n### Build your first NGSI-LD entity\n\n```python\nfrom datetime import datetime\nfrom ngsildclient import Entity\n\n# No context provided => defaults to NGSI-LD Core Context\nentity = Entity("AirQualityObserved", "RZ:Obsv4567")\n\n# Once we\'ve created our entity by calling the Entity() constructor \n# We can add properties thanks to primitives\n\n# tprop() sets a TemporalProperty\nentity.tprop("dateObserved", datetime(2018, 8, 7, 12))\n\n# gprop() sets a GeoProperty : Point, Polygon, ...\nentity.gprop("location", (44, -8))\n\n# prop() is used for other properties\nentity.prop("PM10", 8).prop("NO2", 22, unitcode="GP", userdata={"reliability": 0.95})\n\n# rel() sets a Relationship Property\nentity.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")\n\nentity.pprint()\n```\n\nThe resulting JSON looks like this :\n\n```json\n{\n  "@context": [\n    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"\n  ],\n  "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",\n  "type": "AirQualityObserved",\n  "dateObserved": {\n    "type": "Property",\n    "value": {\n      "@type": "DateTime",\n      "@value": "2018-08-07T12:00:00Z"\n    }\n  },\n  "PM10": {\n    "type": "Property",\n    "value": 8\n  },\n  "NO2": {\n    "type": "Property",\n    "value": 22,\n    "unitCode": "GP",\n    "reliability": 0.95\n  },\n  "location": {\n    "type": "GeoProperty",\n    "value": {\n      "type": "Point",\n      "coordinates": [\n        -8,\n        44\n      ]\n    }\n  },\n  "refPointOfInterest": {\n    "type": "Relationship",\n    "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"\n  }\n}\n```\n\nOnce you\'re satisfied with it, you can save it to a file to share it, for example with the [Smart Data Models Initiative](https://smartdatamodels.org/).\n\n```python\nentity.save("air_quality_sample.jsonld")\n```\n\nOr you can send it to the NGSI-LD Context Broker for creation.\n\n### Interact with the NGSI-LD Orion broker\n\n```python\nfrom ngsildclient import Entity, SmartDataModels, Client\n\n# This time we don\'t create our own entity but download a sample from the Smart Data Models Initiative\nfarm = Entity.load(SmartDataModels.SmartAgri.Agrifood.AgriFarm)\n\n# We can visualize it : here we would like the simplified representation (aka KeyValues)\nfarm.pprint(kv=True)\n\n# We could add/update properties using the prop primitives as we did previously\n# For the sake of example we\'ll just update the phone number, using the dot notation facility\nfarm["contactPoint.value.telephone"] = "00349674538"\n\n# Send it to the Context Broker for creation\n# Here you need a Context Broker up and running\n# You can find some ready-to-use docker-compose files in the brokers/ folder\n# Without any arguments the client targets localhost and the default port\nwith Client() as client:\n    client.create(farm)\n\n# Later you\'ll be able to retrieve the entity from the broker and resend it for update\nwith Client() as client:\n    # retrieve the entity by its id\n    farm = client.retrieve("urn:ngsi-ld:AgriFarm:72d9fb43-53f8-4ec8-a33c-fa931360259a")\n    # It would also work by passing the entity - in case it\'s still in memory\n    # farm = client.retrieve(farm)\n    farm["contactPoint.value.telephone"] = "00349674539"\n    client.update(farm)\n```\n\n## License\n\n[Apache 2.0](LICENSE)\n\n## Documentation\n\nDocstrings are widely used in the code.\n\nFor example.\n\n```python\nfrom ngsildclient import Entity\n\nhelp(Entity)\n```\n\nFor examples (from basic to more complex and realistic) you can have a look at the ``tests`` folder.\n\nEspecially the ``tests/test_entity.py`` file that builds basic entities.\n\nAnd inside the ``tests/smartdatamodels`` folder that builds some sample entities from the Smart Data Models Initiative.\n\n## Roadmap\n\n- Add authentication\n- Extend API coverage : add support for query, batch operations and subscriptions\n- Add documentation\n',
    'author': 'fbattello',
    'author_email': 'fabien.battello@orange.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Orange-OpenSource/python-orion-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
