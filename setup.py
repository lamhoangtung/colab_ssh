#!/usr/bin/env python
import os

from setuptools import find_packages, setup

__version__ = "0.1.5"


def read_me():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()


setup(
    name="linus_colab_ssh",
    version=__version__,
    description='Create SSH tunel to a running colab notebook',
    long_description=read_me(),
    long_description_content_type='text/markdown',
    url='https://github.com/lamhoangtung/colab_ssh',
    author='Hoang Tung Lam',
    author_email='lamhoangtung.vz@gmail.com',
    include_package_data=True,
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    keywords=['ssh', 'colab'],
    setup_requires=[],
    dependency_links=[],
    python_requires='>=3',
    py_modules=['ssh_colab'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
