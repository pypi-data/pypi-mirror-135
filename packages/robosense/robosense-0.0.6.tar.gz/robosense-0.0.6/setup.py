# -*- coding: utf-8 -*-

"""
/*
*
* Auther： Wenjie Zheng <wjzheng@robosense.cn>
* File:    setup.py
*
*/
"""

from setuptools import setup, find_packages

setup(
    name='robosense',
    version='0.0.6',
    keywords=("pip", "robosense"),
    description='robosense lib',
    long_description="This is robosense lib",
    license="MIT Licence",
    url='https://github.com/robosense',
    author='Wenjie Zheng',
    author_email='wjzheng@robosense.cn',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[''],
)
