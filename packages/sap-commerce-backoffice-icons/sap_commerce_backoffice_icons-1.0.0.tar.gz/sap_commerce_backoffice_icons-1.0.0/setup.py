# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sap_commerce_backoffice_icons']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4,<10.0', 'argparse>=1.4.0,<2.0.0', 'numpy>=1.21.3,<2.0.0']

entry_points = \
{'console_scripts': ['backofficeIconConverter = '
                     'sap_commerce_backoffice_icons.backofficeIconConverter:main']}

setup_kwargs = {
    'name': 'sap-commerce-backoffice-icons',
    'version': '1.0.0',
    'description': 'Simple Tool to create explorer tree icons for the SAP Commerce Backoffice interface',
    'long_description': '# SAP Commerce Cloud Backoffice icon converter\n\nSimple Tool to create explorer tree icons for the SAP Commerce Backoffice\ninterface from simple icon files.\n\n## Why is this needed?\n\n![screenshotBackoffice](doc/screenshotBackoffice.png)\n\nThe SAP Commerce Cloud Backoffice interface requires a special crafted sprite\nimage to show it as icon in the explorer tree. This tool helps creating this\nsprites based on a simple icon file.\n\n![overview](doc/overview.png)\n\n## How to use it?\n\nThe simplest case is to convert a single icon. For this you must have an input\nicon meeting the following criterias:\n\n - Size is 16x16 pixels (given by SAP Commerce)\n - Transparent background (otherwise it will not really work)\n - File format should be "png"\n\nRun the following commands to create the sprite (replace the example icon with\nyour own):\n\n```sh\n$ pip install sap-commerce-backoffice-icons\n$ backofficeIconConverter exampleIcons/star.png\nProcess icon exampleIcons/star.png...\nexampleIcons/star.png => exampleIcons/backoffice-star.png\n```\n\nThat\'s it! Now you can use this icon sprite in your custom Backoffice extension\nas icon for your custom types. For more help on how to do this, see\n[Tutorial](doc/Tutorial.md).\n\nYou can also convert multiple icons:\n\n```\n$ backofficeIconConverter ~/FolderWithSomeIcons/* --output converted\n```\n\n\n## Install development environment\n\nTo install the script for development or to run it directly from source, the following\nsteps are needed:\n\n - Install Python >3.7\n - Install Poetry (see https://python-poetry.org/docs/)\n - Make the project ready to be used:\n```sh\ngit clone https://github.com/dev-jan/sap-commerce-backoffice-icons.git\ncd sap-commerce-backoffice-icons\npoetry install\n```\n - Run the script via Poetry virtual env:\n```sh\npoetry run backofficeIconConverter exampleIcons/star.png\n```\n',
    'author': 'Jan Bucher',
    'author_email': 'jan@bucher.cloud',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dev-jan/sap-commerce-backoffice-icons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
