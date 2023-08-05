# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recurse_words', 'recurse_words.recursers']

package_data = \
{'': ['*']}

install_requires = \
['datashader>=0.12.1,<0.13.0',
 'holoviews>=1.14.3,<2.0.0',
 'ipykernel>=5.5.3,<6.0.0',
 'networkx>=2.6.3,<3.0.0',
 'pygraphviz>=1.7,<2.0',
 'requests>=2.25.1,<3.0.0',
 'scikit-image>=0.18.1,<0.19.0',
 'tqdm>=4.60.0,<5.0.0',
 'wheel>=0.36.2,<0.37.0']

extras_require = \
{'docs': ['sphinx>=3.5.4,<4.0.0',
          'furo>=2021.4.11-beta.34,<2022.0.0',
          'autodocsumm>=0.2.2,<0.3.0']}

setup_kwargs = {
    'name': 'recurse-words',
    'version': '0.2.1',
    'description': "find words that have other words in them that when you take the inner words out what's left is still a word",
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/recurse-words/badge/?version=latest)](https://recurse-words.readthedocs.io/en/latest/?badge=latest)\n\n# recurse-words\nfind words that have other words in them that when you remove the inner word what\'s left is still a word\n\n![An example word tree of such a kind](examples/img/collaborationists.png)\n\nand do other stuff too like evaluate the modular phonetic structure of English like\n\n```python\nfrom recurse_words import Graph_Recurser, Graph\nrecurser = Graph_Recurser(\'phonetic_common\')\nrecurser.recurse_all_words(\n    min_include_word = 3,\n    min_test_word    = 2,\n    min_clipped_word = 2\n)\nGraph(recurser).render_graph(\'img\').save(\'/some/path.png\')\n```\n\n![The replacement, addition, and subtraction structure of the phonetic transcription of the 10,000 most common english words](docs/img/shader_phonetic_common_smol.png)\n\n# [docs are here!!!](https://recurse-words.readthedocs.io/en/latest/)\n\nmain docs at https://recurse-words.readthedocs.io/\n```\n   ______________________________\n / \\                             \\.\n|   |      p l e s               |.\n \\_ |        t a k e             |.\n    |          n o t e           |.\n    |     -------------------    |.\n    |                            |.\n    |     this software is       |.\n    |     developed expressly    |.\n    |     for the purpose of     |.\n    |     "funzies"              |.\n    |                            |.\n    |     i make no promises     |.\n    |     that it works          |.\n    |     or is good             |.\n    |                            |.\n    |   _________________________|___\n    |  /                            /.\n    \\_/dc__________________________/.\n```\n\n# installation\n\nFrom pypi:\n\n```\npip install recurse-words\n```\n\nFrom github:\n\n```\ngit clone https://github.com/sneakers-the-rat/recurse-words\npip install ./recurse-words\n# or\npoetry install ./recurse-words\n```\n\n# usage\n\nPoint the recurser at a file that has a list of words,\nfor example [this one](https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt), \nand let \'er rip\n\n```python\nfrom recurse_words import Recurser\n\nrecurser = Recurser(\'path/to/some/words.txt\')\nrecurser.recurse_all_words()\nrecurser.save(\'word_trees.pck\')\n\n# see word trees by a few metrics\n# max tree depth\nrecurser.by_depth\n# total number of leaves\nrecurser.by_leaves\n# total number of edges\nrecurser.by_density\n```\n\nDraw network graphs!\n\n```python\nrecurser.draw_graph(\'some_word\', \'/output/directory\')\n```\n\nAuto-download different corpuses!\n\n```python\nrecurser = Recurser(corpus=\'english\')\nrecurser = Recurser(corpus=\'phonetic\')\n```\n\n',
    'author': 'sneakers-the-rat',
    'author_email': 'JLSaunders987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sneakers-the-rat/recurse-words',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
