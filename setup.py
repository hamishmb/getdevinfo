"""Setup module for GetDevInfo.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='getdevinfo',
    version='1.0.6',
    description='A device information gatherer for Linux and macOS',
    long_description=long_description,

    url='https://www.hamishmb.com/',
    author='Hamish McIntyre-Bhatty',
    author_email='hamishmb@live.co.uk',
    license='GPLv3+',

    classifiers=[
        #The most important stuff.
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        #Python versions.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        #Misc.
        'Environment :: MacOS X',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'

    ],

    keywords='devices hardware',
    packages=find_packages(),
    install_requires=['bs4', 'lxml'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
