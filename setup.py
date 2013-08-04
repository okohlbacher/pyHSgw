# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    )


setup(name='pyhwgs',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        ],
      keywords='',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/zopyx.homeserver',
      license='GNU Public License V2 (GPL 2)',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pyhwgs', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'requests',
                        'lxml',
                        ],
      test_suite = None,
      )
