#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/1/10 4:08 下午
# @Author  : lijiarui
# @Email   : lijiarui15@jd.com
# @Site    : 
# @File    : setup.py
# @Software: PyCharm
import setuptools
import io
import os
import sys
from shutil import rmtree

class UploadCommand(setuptools.Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        sys.exit()

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='UTF-8') as f:
    long_description = '\n' + f.read()

setuptools.setup(
    name='py_nacos_client',
    version='0.1.7',
    author='lijiarui',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description="Python client for Nacos.",
    python_requires='>=3',
    install_requires=[
        'nacos-sdk-python'
    ],
    cmdclass={
        'upload': UploadCommand,
    },
    keywords=['jd_nacos_py',],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)