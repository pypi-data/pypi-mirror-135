# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datagrepper', 'datagrepper.docs']

package_data = \
{'': ['*'],
 'datagrepper': ['static/*',
                 'static/css/*',
                 'static/css/fonts/Bold/*',
                 'static/css/fonts/BoldItalic/*',
                 'static/css/fonts/Italic/*',
                 'static/css/fonts/Light/*',
                 'static/css/fonts/LightItalic/*',
                 'static/css/fonts/Regular/*',
                 'templates/*']}

install_requires = \
['Pygments>=2.9.0,<3.0.0',
 'SQLAlchemy<1.4.23',
 'arrow>=1.1.1,<2.0.0',
 'cffi>=1.14.6,<2.0.0',
 'datanommer.models>=1.0.0,<2.0.0',
 'docutils>=0.17.1,<0.18.0',
 'flask-healthz>=0.0.1,<0.0.2',
 'flask>=1.1,<2.0',
 'moksha.common>=1.2.5,<2.0.0',
 'psycopg2>=2.9.1,<3.0.0',
 'pygal>=2.4.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

extras_require = \
{'deploy': ['gunicorn>=20.0,<21.0'],
 'schemas': ['anitya-schema>=2.0.0,<3.0.0',
             'fedora-messaging-the-new-hotness-schema>=1.1.0,<2.0.0',
             'bodhi-messages>=5.5,<6.0',
             'fedocal-messages>=1.5.0,<2.0.0',
             'fedora-planet-messages>=1.0.0,<2.0.0',
             'noggin-messages>=1.0.0,<2.0.0',
             'fedorainfra-ansible-messages',
             'nuancier-messages>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'datagrepper',
    'version': '1.0.0',
    'description': 'A webapp to query datanommer',
    'long_description': "# datagrepper\n\nDatagrepper is a web application and JSON API to retrieve historical messages sent via Fedora Messaging. [Datanommer](https://github.com/fedora-infra/datanommer/) is a seperate project and service that consumes messages from the Fedora Messaging queue and puts them in a database. These messages is what datagrepper queries. \n\nDatagrepper is curently running in production at https://apps.fedoraproject.org/datagrepper/\n\n## Development Environment\n\nVagrant allows contributors to get quickly up and running with a datagrepper development environment by automatically configuring a virtual machine. \n\nThe datagrepper Vagrant environment configures configures and enables a datanommer service and database. The datanommer instance is configured to be empty when first provisioned, but to consume messages from the stage Fedora Messaging queue.\n\n### Install vagrant\nTo get started, run the following commands to install the Vagrant and Virtualization packages needed, and start the libvirt service:\n\n    $ sudo dnf install ansible libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager\n    $ sudo systemctl enable libvirtd\n    $ sudo systemctl start libvirtd\n\n### Checkout and Provision\nNext, check out the datagrepper code and run vagrant up:\n\n    $ git clone https://github.com/fedora-infra/datagrepper\n    $ cd datanommer\n    $ vagrant up\n\n### Interacting with your development datagrepper\nAfter successful provisioning of the Datagrepper vagrant setup, the datagrepper web application will be accessible from your host machine's web browser at\n\nhttp://datagrepper.test:5000/\n\n\n\n\n### Using the development environment\nSSH into your newly provisioned development environment:\n\n    $ vagrant ssh\n\nThe vagrant setup also defines 4 handy commands to interact with the service that runs the datagrepper flask application: \n\n    $ datagrepper-start\n    $ datagrepper-stop\n    $ datagrepper-restart\n    $ dataprepper-logs\n\nAdditionally, the following commands are also available for interacting with the datanommer service:\n\n    $ datanommer-consumer-start\n    $ datanommer-consumer-stop\n    $ datanommer-consumer-restart\n    $ datanommer-consumer-logs\n\n### Running the tests\nDatanommer is comprised of 3 seperate modules in this single repository. There is a handy script in the top directory of this repo to run the tests on all 3 modules:\n\n    $ ./runtests.sh\n\nHowever, tests can also be run on a single module by invotking tox in that modules' directory. For example:\n\n    $ cd datanommer.models/\n    $ tox\n\nNote, that the tests use virtual environments that are not created from scratch with every subsequent run of the tests. Therefore, **when changes happen to dependencies, the tests may fail to run correctly**. To recreate the virtual envrionments,  run the tests commands with the `-r` flag, for example:\n\n    $ ./runtests.sh -r\n\nor\n\n    $ cd datanommer.models/\n    $ tox -r\n",
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/datagrepper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
