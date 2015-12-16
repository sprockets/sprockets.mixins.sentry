#!/usr/bin/env python

import codecs
import sys

import setuptools


def read_requirements_file(req_name):
    requirements = []
    try:
        with codecs.open(req_name, encoding='utf-8') as req_file:
            for req_line in req_file:
                if '#' in req_line:
                    req_line = req_line[0:req_line.find('#')].strip()
                if req_line:
                    requirements.append(req_line.strip())
    except IOError:
        pass
    return requirements


install_requires = read_requirements_file('requirements.txt')
setup_requires = read_requirements_file('setup-requirements.txt')
tests_require = read_requirements_file('test-requirements.txt')

if sys.version_info < (2, 7):
    tests_require.append('unittest2')
if sys.version_info < (3, 0):
    tests_require.append('mock')

setuptools.setup(
    name='sprockets.mixins.sentry',
    version='0.4.0',
    description='A RequestHandler mixin for sending exceptions to Sentry',
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    url='https://github.com/sprockets/sprockets.mixins.sentry.git',
    author='AWeber Communications',
    author_email='api@aweber.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['sprockets',
              'sprockets.mixins',
              'sprockets.mixins.sentry'],
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    namespace_packages=['sprockets',
                        'sprockets.mixins'],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    zip_safe=False)
