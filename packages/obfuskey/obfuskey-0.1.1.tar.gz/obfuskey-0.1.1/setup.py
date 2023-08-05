# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obfuskey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'obfuskey',
    'version': '0.1.1',
    'description': 'A small library for obfuscating integer values to key strings using a set length and alphabet.',
    'long_description': '# Obfuskey\n\n[![pypi][pypi-v]][pypi] [![license][pypi-l]][pypi] [![coverage][codecov-i]][codecov] [![build][workflow-i]][workflow]\n\nTaking lessons learned from supporting [BaseHash][basehash] over the years, it was\nobvious that it could be optimized, thus Obfuskey was born. BaseHash had some\nmisconceptions, mainly that consumers thought it was a crypto library due to the word \n"hash". Since a hashes are generally irreversible, this new project was born to clearly \nconvey what it is used for.\n\nObfuskey was a way to both modernize and simplify [BaseHash][basehash], while keeping\nthe same functionality. Obfuskey generates obfuscated keys out of integer values that\nhave a uniform length using a specified alphabet. It was built solely for Python 3.6 and\nup. There are no guarantees that it will work for lower versions. If you need this for\na lower version, please use [BaseHash][basehash].\n\nWhen generating keys, the combination of key length and alphabet used will determine the\nmaximum value it can obfuscate, `len(alphabet) ** key_length - 1`.\n\n## Usage\n\nTo use Obfuskey, you can use one of the available alphabets, or provide your own. You\ncan also provide your own multiplier, or leave it blank to use the built-in prime\ngenerator.\n\n```python\nfrom obfuskey import Obfuskey, alphabets\n\nobfuscator = Obfuskey(alphabets.BASE36, key_length=8)\n\nkey = obfuscator.get_key(1234567890)  # FWQ8H52I\nvalue = obfuscator.get_value(\'FWQ8H52I\')  # 1234567890\n```\n\nTo provide a custom multiplier, or if you to provide the prime generated from a\nprevious instance, you can pass it in with `multiplier=`. This value has to be an odd\ninteger.\n\n```python\nfrom obfuskey import Obfuskey, alphabets\n\nobfuscator = Obfuskey(alphabets.BASE62)\nkey = obfuscator.get_key(12345)  # d2Aasl\n\nobfuscator = Obfuskey(alphabets.BASE62, multiplier=46485)\nkey = obfuscator.get_key(12345)  # 0cpqVJ\n```\n\nIf you wish to generate a prime not within the golden prime set, you can overwrite the\nmultiplier with `set_prime_multiplier`.\n\n```python\nfrom obfuskey import Obfuskey, alphabets\n\nobfuscator = Obfuskey(alphabets.BASE62, key_length=2)\nkey = obfuscator.get_key(123)  # 3f\n\nobfuscator.set_prime_multiplier(1.75)\nkey = obfuscator.get_key(123)  # RP\n```\n\n## Extras\n\nIf you need to obfuscate integers that are larger than 512-bit, you will need to also\nhave [gmp2][gmpy2] installed.\n\n```text\n$ pip install gmpy2\n\nOR\n\npoetry install -E gmpy2\n```\n\n[basehash]: https://github.com/bnlucas/python-basehash\n[gmpy2]: https://pypi.org/project/gmpy2/\n[pypi]: https://pypi.python.org/pypi/Obfuskey\n[pypi-v]: https://img.shields.io/pypi/v/Obfuskey.svg\n[pypi-l]: https://img.shields.io/pypi/l/Obfuskey.svg\n[codecov]: https://codecov.io/gh/bnlucas/Obfuskey\n[codecov-i]: https://img.shields.io/codecov/c/github/bnlucas/Obfuskey/master.svg\n[workflow]: https://github.com/bnlucas/Obfuskey/actions?query=branch%3Amain+\n[workflow-i]: https://img.shields.io/github/workflow/status/bnlucas/Obfuskey/CI/main',
    'author': 'Nathan Lucas',
    'author_email': 'nathan@bnlucas.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bnlucas/obfuskey',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
