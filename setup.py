# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    )


setup(name='pyhsgw',
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
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'requests',
                        'plac',
                        'lxml',
                        ],
      entry_points=dict(console_scripts=[
        'hs-find=pyhsgw.hs_find:main',
        'hs-set-value-by-addr=pyhsgw.hs_set_value_by_addr:main',
        'hs-get-value-by-addr=pyhsgw.hs_get_value_by_addr:main',
          ]),
      test_suite = None,
      )
