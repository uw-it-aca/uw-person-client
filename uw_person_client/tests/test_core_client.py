# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from unittest.mock import PropertyMock, call, patch, Mock
from uw_person_client.exceptions import AdviserNotFoundException, \
    PersonNotFoundException
from uw_person_client.clients.core_client import UWPersonClient
from sqlalchemy.orm.exc import NoResultFound


class UWPersonClientTest(TestCase):

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_empty_get_person_by_uwnetid(self, mock_PDS):
        empty_query = None

        mock_first = Mock()
        first_attrs = {'first.return_value': empty_query}
        mock_first.configure_mock(**first_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_first}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_uwnetid, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_uwnetid(self, mock_PDS, mock_map_person):
        query = Mock()

        mock_first = Mock()
        first_attrs = {'first.return_value': query}
        mock_first.configure_mock(**first_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_first}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_person_by_uwnetid('test')
        mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_uwregid_not_found(self, mock_PDS):
        empty_query = None

        mock_first = Mock()
        first_attrs = {'first.return_value': empty_query}
        mock_first.configure_mock(**first_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_first}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_uwregid, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_uwregid(self, mock_PDS, mock_map_person):
        query = Mock()

        mock_first = Mock()
        first_attrs = {'first.return_value': query}
        mock_first.configure_mock(**first_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_first}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_person_by_uwregid('test')
        mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_student_number_not_found(self, mock_PDS):
        empty_query = None

        mock_one_or_none = Mock()
        one_or_none_attrs = {'one_or_none.return_value': empty_query}
        mock_one_or_none.configure_mock(**one_or_none_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_one_or_none}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_student_number, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_student_number(self, mock_PDS, mock_map_person):
        query = Mock()

        mock_one_or_none = Mock()
        one_or_none_attrs = {'one_or_none.return_value': query}
        mock_one_or_none.configure_mock(**one_or_none_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_one_or_none}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_person_by_student_number('test')
        mock_map_person.assert_called_once_with(query)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_system_key_not_found(self, mock_PDS):
        empty_query = None

        mock_one_or_none = Mock()
        one_or_none_attrs = {'one_or_none.return_value': empty_query}
        mock_one_or_none.configure_mock(**one_or_none_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_one_or_none}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(PersonNotFoundException,
                          client.get_person_by_system_key, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_person_by_system_key(self, mock_PDS, mock_map_person):
        query = Mock()

        mock_one_or_none = Mock()
        one_or_none_attrs = {'one_or_none.return_value': query}
        mock_one_or_none.configure_mock(**one_or_none_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_one_or_none}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_person_by_system_key('test')
        mock_map_person.assert_called_once_with(query)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons(self, mock_PDS, mock_map_person):
        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_all}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_persons()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_registered_students(self, mock_PDS, mock_map_person):
        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_all}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_registered_students()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_active_students(self, mock_PDS, mock_map_person):
        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_all}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_active_students()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_active_employees(self, mock_PDS, mock_map_person):
        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_all}
        mock_filter.configure_mock(**filter_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_filter}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_active_employees()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_advisers(self, mock_PDS, mock_map_person):
        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_all}
        mock_join.configure_mock(**join_attrs)

        mock_join2 = Mock()
        join2_attrs = {'join.return_value': mock_join}
        mock_join2.configure_mock(**join2_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join2}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_advisers()
        mock_map_person.assert_has_calls(calls)

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_advisers_with_program(self, mock_PDS, mock_map_person):
        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query}
        mock_all.configure_mock(**all_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_all,
                        'join.return_value': mock_filter}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_advisers(advising_program='test')
        mock_map_person.assert_has_calls(calls)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_netid_not_found(self, mock_PDS):
        mock_query = Mock()
        query_attrs = {'session.query.side_effect': NoResultFound}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(AdviserNotFoundException,
                          client.get_persons_by_adviser_netid, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_netid(self, mock_PDS, mock_map_person):
        adviser_mock = Mock()
        mock_id = PropertyMock(return_value=1)
        type(adviser_mock).adviser_id = mock_id

        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query,
                     'one.return_value': adviser_mock}
        mock_all.configure_mock(**all_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_all,
                        'join.return_value': mock_filter}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_persons_by_adviser_netid('test')
        mock_map_person.assert_has_calls(calls)

    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_regid_not_found(self, mock_PDS):
        mock_query = Mock()
        query_attrs = {'session.query.side_effect': NoResultFound}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        self.assertRaises(AdviserNotFoundException,
                          client.get_persons_by_adviser_regid, 'test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_persons_by_adviser_regid(self, mock_PDS, mock_map_person):
        adviser_mock = Mock()
        mock_id = PropertyMock(return_value=1)
        type(adviser_mock).adviser_id = mock_id

        query = [Mock(), Mock()]
        calls = [call(q) for q in query]

        mock_all = Mock()
        all_attrs = {'all.return_value': query,
                     'one.return_value': adviser_mock}
        mock_all.configure_mock(**all_attrs)

        mock_filter = Mock()
        filter_attrs = {'filter.return_value': mock_all,
                        'join.return_value': mock_filter}
        mock_filter.configure_mock(**filter_attrs)

        mock_join = Mock()
        join_attrs = {'join.return_value': mock_filter}
        mock_join.configure_mock(**join_attrs)

        mock_query = Mock()
        query_attrs = {'session.query.return_value': mock_join}
        mock_query.configure_mock(**query_attrs)

        mock_PDS.return_value = mock_query
        client = UWPersonClient()
        client.get_persons_by_adviser_regid('test')
        mock_map_person.assert_has_calls(calls)
