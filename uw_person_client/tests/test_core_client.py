# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from unittest.mock import PropertyMock, call, patch, MagicMock
from uw_person_client.exceptions import AdviserNotFoundException, \
    PersonNotFoundException
from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.components import Person
from sqlalchemy.orm.exc import NoResultFound


class UWPersonClientTest(TestCase):

    def _get_query_string(self, joins=0, filters=0, first=False, all=False,
                          one=False, one_or_none=False):
        query_string = "session.query.return_value"
        for i in range(joins):
            query_string += ".join.return_value"
        for i in range(filters):
            query_string += ".filter.return_value"
        if first:
            query_string += ".first.return_value"
        if all:
            query_string += ".all.return_value"
        if one:
            query_string += ".one.return_value"
        if one_or_none:
            query_string += ".one_or_none.return_value"
        return query_string

    def _create_mock_query(self, result, **kwargs):
        mock_query = MagicMock()

        query_string = self._get_query_string(**kwargs)
        query_attrs = {query_string: result}
        mock_query.configure_mock(**query_attrs)
        return mock_query

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_empty_get_person_by_uwnetid(self, mock_PDS):
        empty_query = None
        mock_query = self._create_mock_query(empty_query, filters=1,
                                             first=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_uwnetid, 'test')

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_uwnetid(self, mock_PDS):
        query = MagicMock()
        mock_query = self._create_mock_query(query, filters=1, first=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        result = client.get_person_by_uwnetid('test')
        self.assertIsInstance(result, Person)

        with patch.object(UWPersonClient, '_map_person') as mock_map_person:
            mock_map_person.return_value = 'test'
            result = client.get_person_by_uwnetid('test')
            self.assertEqual(result, 'test')
            mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_uwregid_not_found(self, mock_PDS):
        empty_query = None
        mock_query = self._create_mock_query(empty_query, filters=1,
                                             first=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_uwregid, 'test')

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_uwregid(self, mock_PDS):
        query = MagicMock()
        mock_query = self._create_mock_query(query, filters=1, first=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        result = client.get_person_by_uwregid('test')
        self.assertIsInstance(result, Person)

        with patch.object(UWPersonClient, '_map_person') as mock_map_person:
            mock_map_person.return_value = 'test'
            result = client.get_person_by_uwregid('test')
            self.assertEqual(result, 'test')
            mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_student_number_not_found(self, mock_PDS):
        empty_query = None
        mock_query = self._create_mock_query(empty_query, joins=1, filters=1,
                                             one_or_none=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_student_number, 'test')

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_student_number(self, mock_PDS):
        query = MagicMock()
        mock_query = self._create_mock_query(query, joins=1, filters=1,
                                             one_or_none=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        result = client.get_person_by_student_number('test')
        self.assertIsInstance(result, Person)

        with patch.object(UWPersonClient, '_map_person') as mock_map_person:
            mock_map_person.return_value = 'test'
            result = client.get_person_by_student_number('test')
            self.assertEqual(result, 'test')
            mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_system_key_not_found(self, mock_PDS):
        empty_query = None
        mock_query = self._create_mock_query(empty_query, joins=1, filters=1,
                                             one_or_none=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_system_key, 'test')

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_system_key(self, mock_PDS):
        query = MagicMock()
        mock_query = self._create_mock_query(query, joins=1, filters=1,
                                             one_or_none=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        result = client.get_person_by_system_key('test')
        self.assertIsInstance(result, Person)

        with patch.object(UWPersonClient, '_map_person') as mock_map_person:
            mock_map_person.return_value = 'test'
            result = client.get_person_by_system_key('test')
            self.assertEqual(result, 'test')
            mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons(self, mock_PDS):
        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]
        mock_query = self._create_mock_query(query, all=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        result = client.get_persons()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Person)

        with patch.object(UWPersonClient, '_map_person') as mock_map_person:
            mock_map_person.return_value = 'test'
            result = client.get_persons()
            self.assertEqual(result, ['test', 'test'])
            mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_registered_students(self, mock_PDS, mock_map_person):
        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]
        mock_query = self._create_mock_query(query, joins=1, filters=1,
                                             all=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_registered_students()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_active_students(self, mock_PDS, mock_map_person):
        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]
        mock_query = self._create_mock_query(query, filters=1, all=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_active_students()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_active_employees(self, mock_PDS, mock_map_person):
        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]
        mock_query = self._create_mock_query(query, filters=1, all=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_active_employees()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_advisers(self, mock_PDS, mock_map_person):
        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]
        mock_query = self._create_mock_query(query, joins=2, all=True)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_advisers()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_advisers_with_program(self, mock_PDS, mock_map_person):
        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]

        mock_all = MagicMock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_filter = MagicMock()
        filter_attrs = {'filter.return_value': mock_all,
                        'join.return_value': mock_filter}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = MagicMock()
        query_attrs = {self._get_query_string(joins=1): mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_advisers(advising_program='test')
        mock_map_person.assert_has_calls(calls)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_netid_not_found(self, mock_PDS):
        mock_query = MagicMock()
        query_attrs = {'session.query.side_effect': NoResultFound}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(AdviserNotFoundException,
                          client.get_persons_by_adviser_netid, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_netid(self, mock_PDS, mock_map_person):
        adviser_mock = MagicMock()
        mock_id = PropertyMock(return_value=1)
        type(adviser_mock).adviser_id = mock_id

        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]

        mock_all = MagicMock()
        all_attrs = {'all.return_value': query,
                     'one.return_value': adviser_mock}
        mock_all.configure_mock(**all_attrs)

        mock_filter = MagicMock()
        filter_attrs = {'filter.return_value': mock_all,
                        'join.return_value': mock_filter}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = MagicMock()
        query_attrs = {self._get_query_string(joins=1): mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_persons_by_adviser_netid('test')
        mock_map_person.assert_has_calls(calls)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_regid_not_found(self, mock_PDS):
        mock_query = MagicMock()
        query_attrs = {'session.query.side_effect': NoResultFound}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(AdviserNotFoundException,
                          client.get_persons_by_adviser_regid, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_regid(self, mock_PDS, mock_map_person):
        adviser_mock = MagicMock()
        mock_id = PropertyMock(return_value=1)
        type(adviser_mock).adviser_id = mock_id

        query = [MagicMock(), MagicMock()]
        calls = [call(q) for q in query]

        mock_all = MagicMock()
        all_attrs = {'all.return_value': query,
                     'one.return_value': adviser_mock}
        mock_all.configure_mock(**all_attrs)

        mock_filter = MagicMock()
        filter_attrs = {'filter.return_value': mock_all,
                        'join.return_value': mock_filter}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = MagicMock()
        query_attrs = {self._get_query_string(joins=1): mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_persons_by_adviser_regid('test')
        mock_map_person.assert_has_calls(calls)
