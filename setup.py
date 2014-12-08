from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

setup(
    name='PyVDF',
    version='1.0.2',
    py_modules=['PyVDF'],
    url='https://github.com/noriah/PyVDF',
    license='MIT',
    author='noriah',
    author_email='vix@noriah.dev',
    keywords = "VDF KeyValues Valve",
    description='Python Library for reading VDFs and Valve KeyValue files',
    long_description=read('README.rst'),
    platforms='any',
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