#!/usr/bin/env python

import codecs

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


install_requires = read_requirements_file('requires/installation.txt')
tests_require = read_requirements_file('requires/testing.txt')

setuptools.setup(
    name='sprockets.mixins.sentry',
    version='1.2.0',
    description='A RequestHandler mixin for sending exceptions to Sentry',
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
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
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    zip_safe=False)
