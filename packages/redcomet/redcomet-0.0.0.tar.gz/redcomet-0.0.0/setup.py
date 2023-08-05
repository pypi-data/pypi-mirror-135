import setuptools
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

NAME = 'redcomet'
VERSION = '0.0.0'
URL = 'https://github.com/SSripilaipong/redcomet'
LICENSE = 'MIT'
AUTHOR = 'SSripilaipong'
EMAIL = 'SHSnail@mail.com'

setup(
    name=NAME,
    version=VERSION,
    packages=[p for p in setuptools.find_packages() if p.startswith('redcomet.') or p == 'redcomet'],
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=None,
    long_description=None,
    python_requires='>=3.6',
    install_requires=requirements,
    classifiers=[],
    include_package_data=True,
)
