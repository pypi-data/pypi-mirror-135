# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2022/01/17 11:04:08
@Author  :   ufy
@Contact :   antarm@outlook.com
@Version :   v1.0
@Desc    :   None
'''

# here put the import lib
from setuptools import setup,find_packages


setup(
    name = 'ufy',
    version = '0.1.15',
    description= 'some tools for ufy',
    author='ufy',
    author_eamil='antarm@outlook.com',
    packages=find_packages('.'),
)

# print(find_packages('.'),)