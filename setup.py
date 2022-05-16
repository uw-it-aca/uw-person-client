import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/axdd-person-client>`_.
"""

version_path = 'uw_person_client/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='axdd-person-client',
    verson=VERSION,
    packages=['uw_person_client'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=['commonconf',
                      'mock',
                      'psycopg2-binary',
                      'SQLAlchemy==1.0.14',
                     ],
    license='Apache License, Version 2.0',
    description=('A library for connecting to and querying the '
                 'uw-person-datastore'),
    long_description=README,
    url='https://github.com/uw-it-aca/axdd-person-client',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
