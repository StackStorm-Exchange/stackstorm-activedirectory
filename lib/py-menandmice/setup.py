import os.path

from setuptools import setup, find_packages

from dist_utils import fetch_requirements
from dist_utils import apply_vagrant_workaround

from menandmice import __version__

PACKAGE_NAME = 'menandmice'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, 'requirements.txt')

install_reqs, dep_links = fetch_requirements(REQUIREMENTS_FILE)

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=PACKAGE_NAME,
    version=__version__,
    description='Python bindings for the Men&Mice IPAM REST API ',
    long_description=readme,
    author='Encore Technologies',
    author_email='code@encore.tech',
    url='https://github.com/EncoreTechnologies/py-menandmice'
    license=license,
    install_requires=install_reqs,
    dependency_links=dep_links,
    test_suite=PACKAGE_NAME,
    packages=find_packages(exclude=['tests'])
)
