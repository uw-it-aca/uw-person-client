# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from commonconf.backends import use_configparser_backend
from os.path import abspath, dirname
import os

if __name__ == '__main__':
    path = abspath(os.path.join(dirname(__file__),
                                "..", "conf", "test.conf"))
    use_configparser_backend(path, "UW_PERSON_CLIENT")

    from nose2 import discover
    discover()
