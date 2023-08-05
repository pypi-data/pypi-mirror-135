# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaaredis', 'yaaredis.commands']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['contextvars>=1.0.0,<3.0.0'],
 'hiredis': ['hiredis>=0.2.0,<3.0.0']}

setup_kwargs = {
    'name': 'yaaredis',
    'version': '3.0.0',
    'description': 'Python async client for Redis key-value store',
    'long_description': "talkiq/yaaredis\n===============\n\n|circleci| |pypi-version| |python-versions|\n\n.. |circleci| image:: https://img.shields.io/circleci/project/github/talkiq/yaaredis/master.svg?style=flat-square\n    :alt: CircleCI Test Status\n    :target: https://circleci.com/gh/talkiq/yaaredis/tree/master\n\n.. |pypi-version| image:: https://img.shields.io/pypi/v/yaaredis.svg?style=flat-square&label=PyPI\n    :alt: Latest PyPI Release\n    :target: https://pypi.org/project/yaaredis/\n\n.. |python-versions| image:: https://img.shields.io/pypi/pyversions/yaaredis.svg?style=flat-square&label=Python%20Versions\n    :alt: Compatible Python Versions\n    :target: https://pypi.org/project/yaaredis/\n\n``yaaredis`` (Yet Another Async Redis (client)) is a fork of\n`aredis <https://github.com/NoneGG/aredis>`_, which itself was ported from\n`redis-py <https://github.com/andymccurdy/redis-py>`_. ``yaaredis`` provides an\nefficient and user-friendly async redis client with support for Redis Server,\nCluster, and Sentinels.\n\nTo get more information please read the `full documentation`_ managed by the\nupstream ``aredis`` repo. We are working on hosting our own as the projects\ndiverge -- stay tuned!\n\nInstallation\n------------\n\n``yaaredis`` requires a running Redis server. To install yaaredis, simply:\n\n.. code-block:: console\n\n    python3 -m pip install yaaredis\n\nor from source:\n\n.. code-block:: console\n\n    python3 -m pip install .\n\nNote that ``yaaredis`` also supports using ``hiredis`` as a drop-in performance\nimprovements. You can either install ``hiredis`` separately or make use of the\nPyPI extra to make use of this functionality:\n\n.. code-block:: console\n\n    python3 -m pip install yaaredis[hiredis]\n\nGetting started\n---------------\n\nWe have `various examples`_ in this repo which you may find useful. A few more\nspecific cases are listed below.\n\nSingle Node Client\n^^^^^^^^^^^^^^^^^^\n\n.. code-block:: python\n\n    import asyncio\n    from yaaredis import StrictRedis\n\n    async def example():\n        client = StrictRedis(host='127.0.0.1', port=6379, db=0)\n        await client.flushdb()\n        await client.set('foo', 1)\n        assert await client.exists('foo') is True\n        await client.incr('foo', 100)\n\n        assert int(await client.get('foo')) == 101\n        await client.expire('foo', 1)\n        await asyncio.sleep(0.1)\n        await client.ttl('foo')\n        await asyncio.sleep(1)\n        assert not await client.exists('foo')\n\n    asyncio.run(example())\n\nCluster Client\n^^^^^^^^^^^^^^\n\n.. code-block:: python\n\n    import asyncio\n    from yaaredis import StrictRedisCluster\n\n    async def example():\n        client = StrictRedisCluster(host='172.17.0.2', port=7001)\n        await client.flushdb()\n        await client.set('foo', 1)\n        await client.lpush('a', 1)\n        print(await client.cluster_slots())\n\n        await client.rpoplpush('a', 'b')\n        assert await client.rpop('b') == b'1'\n\n    asyncio.run(example())\n    # {(10923, 16383): [{'host': b'172.17.0.2', 'node_id': b'332f41962b33fa44bbc5e88f205e71276a9d64f4', 'server_type': 'master', 'port': 7002},\n    # {'host': b'172.17.0.2', 'node_id': b'c02deb8726cdd412d956f0b9464a88812ef34f03', 'server_type': 'slave', 'port': 7005}],\n    # (5461, 10922): [{'host': b'172.17.0.2', 'node_id': b'3d1b020fc46bf7cb2ffc36e10e7d7befca7c5533', 'server_type': 'master', 'port': 7001},\n    # {'host': b'172.17.0.2', 'node_id': b'aac4799b65ff35d8dd2ad152a5515d15c0dc8ab7', 'server_type': 'slave', 'port': 7004}],\n    # (0, 5460): [{'host': b'172.17.0.2', 'node_id': b'0932215036dc0d908cf662fdfca4d3614f221b01', 'server_type': 'master', 'port': 7000},\n    # {'host': b'172.17.0.2', 'node_id': b'f6603ab4cb77e672de23a6361ec165f3a1a2bb42', 'server_type': 'slave', 'port': 7003}]}\n\nBenchmark\n---------\n\nPlease run test scripts in the ``benchmarks`` directory to confirm the\nbenchmarks. For a benchmark in the original yaaredis author's environment\nplease see: `benchmark`_.\n\nContributing\n------------\n\nDeveloper? See our `guide`_ on how you can contribute.\n\n.. _benchmark: http://aredis.readthedocs.io/en/latest/benchmark.html\n.. _full documentation: http://aredis.readthedocs.io/en/latest/\n.. _guide: https://github.com/talkiq/yaaredis/blob/master/.github/CONTRIBUTING.rst\n.. _various examples: https://github.com/talkiq/yaaredis/tree/master/examples\n",
    'author': 'Vi Engineering',
    'author_email': 'voiceai-eng@dialpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/talkiq/yaaredis',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
