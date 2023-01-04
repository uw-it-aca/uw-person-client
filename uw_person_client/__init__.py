# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
import os

# setup logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ])

if os.environ.get("AXDD_PERSON_CLIENT_ENV") == "PROD":
    from uw_person_client.clients.core_client import UWPersonClient
else:
    from uw_person_client.clients.mock_client import \
        MockedUWPersonClient as UWPersonClient  # noqa
