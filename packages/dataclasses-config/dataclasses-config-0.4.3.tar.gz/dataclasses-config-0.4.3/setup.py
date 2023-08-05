# noinspection PyProtectedMember
from setuptools import _install_setup_requires
_install_setup_requires(dict(setup_requires=[ 'extended-setup-tools' ]))

from extended_setup import ExtendedSetupManager
ExtendedSetupManager('dataclasses_config').setup \
(
    name = 'dataclasses-config',
    url = 'https://gitlab.com/Hares-Lab/dataclasses-config',
    license = "BSD 2-Clause License",
    short_description = "A simple library extension for HOCON configs",
    min_python_version = '3.6.0',
    classifiers =
    [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
