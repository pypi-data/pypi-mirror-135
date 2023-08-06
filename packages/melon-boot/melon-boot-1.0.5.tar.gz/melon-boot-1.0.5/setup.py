# -*- encoding: utf-8 -*-
"""
@Author  : zh_o
"""
from setuptools import setup, find_packages


setup(
    name='melon-boot',
    version='1.0.5',
    author='zh_o',
    author_email='a1763041057@gmail.com',
    description='The uiautomation framework',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['toml', 'selenium', 'pytest', 'allure-pytest', 'faker']
)
