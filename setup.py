from setuptools import setup
from setuptools.command.test import test as TestCommand
import PyVDF
import sys
import codecs
import os

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='PyVDF',
    version=PyVDF.__version__,
    tests_require=['pytest'],
    packages= ['PyVDF'],
    license='MIT',
    url='https://github.com/noriah/PyVDF',
    author='noriah',
    author_email='vix@noriah.dev',
    keywords = "VDF KeyValues Valve",
    description='Python Library for reading VDFs and Valve KeyValue files',
    platforms='any',
    cmdclass={'test': PyTest},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ]
)