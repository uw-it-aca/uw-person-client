# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.session import sessionmaker


class AbstractDatabase(object):

    engine = None
    Base = None

    def __init__(self, expire_session_on_commit=True):
        self._session_factory = sessionmaker(
            expire_on_commit=expire_session_on_commit)
        self._session = None
        self.create_engine()
        self.create_base()

    def create_engine(self):
        raise NotImplementedError()

    def create_base(self):
        AbstractDatabase.Base = automap_base()
        AbstractDatabase.Base.prepare(self.engine, reflect=True)

    @property
    def session(self):
        if self._session is None:
            self._session = self._session_factory(bind=self.engine)
        return self._session

    def commit_session(self):
        try:
            self.session.commit()
        except Exception as e:
            logging.error(e)
            self.session.rollback()
            raise
