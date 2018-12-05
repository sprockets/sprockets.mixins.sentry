#!/usr/bin/env python

import pathlib

import setuptools


REPO = pathlib.Path(__file__).parent


setuptools.setup(
    name='sprockets.mixins.sentry',
    description='A RequestHandler mixin for sending exceptions to Sentry',
    long_description=REPO.joinpath('README.rst').read_text(),
    url='https://github.com/sprockets/sprockets.mixins.sentry.git',
    author='AWeber Communications',
    author_email='api@aweber.com',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.5',
    packages=['sprockets',
              'sprockets.mixins',
              'sprockets.mixins.sentry'],
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    namespace_packages=['sprockets',
                        'sprockets.mixins'],
    install_requires=REPO.joinpath('requires/installation.txt').read_text(),
    tests_require=REPO.joinpath('requires/testing.txt').read_text(),
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    test_suite='nose.collector',
    zip_safe=False)
