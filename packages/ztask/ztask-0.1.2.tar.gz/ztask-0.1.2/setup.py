# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ztask']
install_requires = \
['pandas>=1.3.5,<2.0.0', 'parsedatetime>=2.6,<3.0', 'prettyprint>=0.1.5,<0.2.0']

entry_points = \
{'console_scripts': ['ztask = ztask:main']}

setup_kwargs = {
    'name': 'ztask',
    'version': '0.1.2',
    'description': 'Ztask, the terminal interface to log task in zohoprojects and complete the damned timesheets with a Taskwarrior inspired syntax.',
    'long_description': '\n\n<p align="center">\n  <img src="/images/use_example.png">\n</p>\n\n# <b>Ztask</b>\n\n<b>Ztask</b> helps to log task in <a href="https://projects.zoho.eu" target="_top">zohoprojects</a> and complete the \ndamned timesheets from the terminal using a \n<a href="https://taskwarrior.org/" target="_top">Taskwarrior</a> inspired syntax.\n\nThis little program is made by and for terminal enthusiasts, <b>enjoy it!</b>\n\n## Requirements\n\nYou only need a distribution of python3 installed.\n\n## ⚙️Installation:\n\nYou can install the requirements (preferably in an environment) using:\n\n> pip install ztask\n\nDownload directly the script and set the variables at your user path in .ztask/env_variables.py, \nmore details about these variables bellow.\n \nIf you install "ztask" in a environment you will need to initialize the environment before using ztask, \nfor so sometimes is convenient to use an alias like:\n\n> alias eztask=\'conda activate <env_name> && ztask\'\n\n## Usage:\n\nZtask, as it should be, is a <b>terminal user interface</b> that can be run with:\n\n>python3 ztask.py (in the path) \n\nOr more conveniently using the alias <b>ztask</b>:\n\nFor printing my zoho task:\n\n> ztask\n\nShows all the table, without truncating the table:\n\n> ztask long\n\nLog the task in zoho:\n\n> ztask log number_of_task \'date\' hh:mm\n\nZtask date suports natural language such as: \'today\', \'yesterday\' etc\n\n## Examples:\n\nLog the task 4, two days ago with a duration of 7:30 hours:\n\n> ztask log 4 \'2 days ago\' 07:30 \n\nLog the taks 12 today 8 hours:\n\n> ztask log 12 \'today\' 08:00\n\n## 💾 env variables\n\nFor using the program you will need to create a folder called .ztask in your user path and a file called .ztask \nthe path would look something like: \n\n> C:\\\\Users\\\\YOUR USER NAME\\\\.ztask\\\\ztask.ini\n\nOr in Unix based systems:\n\n> /home/YOUR USER NAME/.ztask/ztask.ini\n\nSet the following env variables in the env_variables.py file (copy paste and fill):\n\n`[variables]`\n\n`client_id = <YOUR CLIENT ID> `\n\n`client_secret = <YOUR CLIENT SECRET> `\n\n`refresh_token = <YOUR REFRESH TOKEN>`\n\n`user_id = <YOUR USER ID>`\n\nThese variables can be found at https://api-console.zoho.eu after creating a self client.\n\nYou can get your refresh_token after getting the grant token. Go to self client same web and generate the grant token\nusing the scope:\n\n`ZohoProjects.tasks.ALL,ZohoProjects.timesheets.ALL,ZohoProjects.projects.ALL,ZohoProjects.portals.READ,ZohoProjects.bugs.ALL`\n\nCopy the grant_token and execute in the terminal:\n\n> ztask get_refresh_token <YOUR GRANT TOKEN>\n\nThe user_id can be found at zoho projects, clicking in the right corner (user icon)\n\n## other\n\nFor checking the formatted documentation:\n\n> pip install mdv \n> mdv readme.md\n\n',
    'author': 'Pablo Ruiz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PabloRuizCuevas/ztask',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
