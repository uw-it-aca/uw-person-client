# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import glob
import os
from uw_person_client.clients import AbstractUWPersonClient
from uw_person_client.components import Person
from uw_person_client.exceptions import PersonNotFoundException


class MockedUWPersonClient(AbstractUWPersonClient):

    def _glob_fixture_file(self, search_value):
        abspath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../fixtures/'))
        path = os.path.join(abspath, search_value)
        return glob.glob(path, recursive=True)

    def _read_person_file(self, search_value):
        try:
            file_name = self._glob_fixture_file(search_value)[0]
        except IndexError:
            raise PersonNotFoundException()
        data = json.load(open(file_name))
        return Person().from_dict(data)

    def _read_person_files(self, search_value):
        file_names = self._glob_fixture_file(search_value)
        persons = []
        for file_name in file_names:
            data = self._read_person_file(file_name)
            persons.append(Person().from_dict(data))
        return persons

    def _read_caseload_file(self, search_value):
        file_name = self._glob_fixture_file('**/_caseloads.json')[0]
        caseload = json.load(open(file_name))
        persons = []
        for adviser_key, student_file_list in caseload.items():
            if search_value in adviser_key:
                for student_file in student_file_list:
                    persons.append(
                        self._read_person_file(f'**/students/{student_file}'))
        return persons

    def get_person_by_uwnetid(self, uwnetid):
        return self._read_person_file(f'**/*{uwnetid}*.json')

    def get_person_by_uwregid(self, uwregid):
        return self._read_person_file(f'**/*{uwregid}*.json')

    def get_person_by_student_number(self, student_number):
        return self._read_person_file(f'**/*{student_number}*.json')

    def get_persons(self, page=None, page_size=None):
        return self._read_person_files('**/[!_]*.json')

    def get_active_students(self, page=None, page_size=None):
        return self._read_person_files('**/students/[!_]*.json')

    def get_active_employees(self, page=None, page_size=None):
        return self._read_person_files('**/employees/[!_]*.json')

    def get_advisers(self, page=None, page_size=None):
        return self._read_person_files('**/advisers/[!_]*.json')

    def get_persons_by_adviser_netid(self, uwnetid):
        return self._read_caseload_file(uwnetid)

    def get_persons_by_adviser_retid(self, uwregid):
        return self._read_caseload_file(uwregid)
