#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'pyyaml', 'wheel' ]

setup(
    author="John Griffiths",
    author_email='gnuchu@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Helper library that converts numbers to words",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='n2w',
    name='numutils.n2w',
    packages=find_packages(include=['numutils', 'numutils']),
    package_data={'numutils': ['config/*.yaml']},
    test_suite='tests',
    url='https://github.com/gnuchu/numutils.n2w',
    version = '0.1.3',
    zip_safe=False,
)
