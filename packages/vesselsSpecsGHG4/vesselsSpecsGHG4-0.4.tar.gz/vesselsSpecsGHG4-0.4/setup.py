# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 00:57:05 2022

@author: gabri
"""

from setuptools import setup, find_packages


setup(
    name='vesselsSpecsGHG4',
    version='0.4',
    license='MIT',
    author="Gabriel Fuentes",
    author_email='gabriel.fuentes@snf.no',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url="https://github.com/gabrielfuenmar/vesselsSpecsGHG4",
    keywords='GHG4adapter',
    install_requires=[
          'scikit-learn',
          'pandas'
      ],

)
