# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webgenesis']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['webgenesis = webgenesis.webgenesis:main']}

setup_kwargs = {
    'name': 'webgenesis',
    'version': '0.0.2',
    'description': 'create basic hello-world apps for the various web frameworks as boiler plates',
    'long_description': "### Webgenesis\nA simple command line interface for generating hello-world starter apps for \nquick setup\n\n\n#### Why Webgenesis?\nWhen building web apps, it can become common to be starting from the same or similar set of code and basic project structure. Hence webgenesis comes in to\nreduce this burden of writing the same code when starting up a web project\n\n\n\n#### Installation\n```bash\npip install webgenesis\n```\n\n\n#### Usage\n```bash\nwebgenesis --help\n\n```\n\n\n#### Create A Project for a web framework\n+ Uses the default 'hello-<webframework>' as project folder\n+ Supported frameworks include\n\t- flask\n\t- streamlit\n\t- express\n\t- koajs\n\t- bottle\n\t- tornado\n\t- fastapi\n\n```bash\nwebgenesis create flask\n\n```\n\n```bash\nwebgenesis create streamlit\n\n```\n\n#### Create A Project using Custom/Specified Project\n```bash\nwebgenesis create flask -f myflaskapp\n```\n\n\n\n#### About\n+ Maintainer: Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n\n\n#### Contributions\nContributions are welcome. In case you notice a bug let us know.\nHappy Coding\n",
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jcharistech/webgenesis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
