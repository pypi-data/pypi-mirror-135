# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.50.3,<0.51.0', 'lectern>=0.18.2,<0.19.0', 'mecha>=0.34.0,<0.35.0']

setup_kwargs = {
    'name': 'lepsen-core',
    'version': '0.2.0rc2',
    'description': 'Minecraft data pack utility library.',
    'long_description': '# Lepsen Core\n\nData pack utility library packaged as a [Beet](https://github.com/mcbeet/beet) plugin.\n\n## Example Beet Configuration\n\nNote that any directly required feature must be manually specified for it to be included in the generated data pack.\nImplicit dependencies of a required feature will be loaded automatically, however, so users of the tick scheduler or forceloaded chunk need not enable the `main` feature.\n\n```yaml\npipeline:\n  - lepsen.core\nmeta:\n  lepsen:\n    main: true\n    forceload: true\n    tick_scheduler: true\n    player_head: true\ndata_pack:\n  name: Example\n  load: ["src/*"]\n```\n\n## Data Pack Initialization\n\nThis pack uses [Lantern Load](https://github.com/LanternMC/load), but the recommended way to check for correct pack initialization is through *compatibility flags*.\nThe benefit of this approach is that a new major version may not break usage of a feature, making this a more flexible way of checking for successful dependency loading.\n\nAn example of minimal initialization of this pack is as follows (including the correct way to check for compatibility flags).\n\n`@function_tag(merge) load:load`\n\n```json\n{\n    "values": [\n        {"id": "#lepsen:core/load", "required": false},\n        "example:load"\n    ]\n}\n```\n\n`@function example:load`\n\n```mcfunction\nexecute\n    if score #lepsen_core.compat load.status matches 1\n    if data storage lepsen:core compat{\n        objectives: 1,\n        forceload: 1\n    }\n    run function example:init\n```\n\n`@function example:init`\n\n```mcfunction\n# Indicate that the plack was successfully loaded.\nscoreboard players set example_pack load.status 1\n\n# Pack initialization logic.\n# ...\n```\n\n## License\n\nLepsen Core is made freely available under the terms of the [0BSD License](LICENSE).\nThird-party contributions shall be licensed under the same terms unless explicitly stated otherwise.\n',
    'author': 'Lue',
    'author_email': 'lue@lued.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luexa/lepsen-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
