"""Setup module for GetDevInfo.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='getdevinfo',
    version='1.0.1',
    description='A device information gatherer for Linux and macOS',
    long_description='Working on both Linux and macOS, this script makes use of lshw, lvdisplay, and blkid (Linux), as well as diskutil (macOS) to get a comprehensive amount of disk information. This information is available in a structured dictionary for ease of use. On Linux it requires lshw, blkid, and lvdisplay to be installed. On Linux, you need beautifulsoup4 (bs4) to use this tool. On macOS, nothing beyond a standard python2.x/python3.x install is required, but you still need bs4 if you want to install using the python wheel/through pip.',

    url='https://www.github.com/hamishmb/getdevinfo',
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
    install_requires=['bs4'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
