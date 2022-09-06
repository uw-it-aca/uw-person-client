# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from unittest.mock import PropertyMock, call, patch, Mock, MagicMock
from uw_person_client.exceptions import AdviserNotFoundException, \
    PersonNotFoundException
from uw_person_client.clients.core_client import UWPersonClient
from sqlalchemy.orm.exc import NoResultFound


class UWPersonClientTest(TestCase):

    @patch('uw_person_client.clients.core_client.UWPDS')
    def get_mock_person_client(self, mock_uwpds):
        client = UWPersonClient()
        client.DB = mock_uwpds.return_value
        return client

    @patch('uw_person_client.clients.core_client.UWPersonClient._map_person')
    def test_get_person_by_uwnetid(self, mock_map_person):
        client = self.get_mock_person_client()
        # person exists
        mock_person = MagicMock()
        mock_netid = 'test',
        client.DB.session.query.return_value.filter.return_value.first = \
            MagicMock(return_value=mock_person)

        return_value = client.get_person_by_uwnetid(mock_netid, arg1='arg1')
        # assertions
        client.DB.session.query.assert_called_once_with(
            client.DB.HistoricalPerson)
        client.DB.session.query.return_value.filter.assert_called_once_with(
            client.DB.HistoricalPerson.prior_uwnetid == mock_netid)
        client.DB.session.query.return_value.filter.return_value.first.\
            assert_called_once()
        self.assertEqual(
            return_value, mock_map_person(mock_person, arg1='arg1'))

        # no person found
        client.DB.session.query.return_value.filter.return_value.first = \
            MagicMock(return_value=None)
        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_uwnetid(mock_netid)

    @patch('uw_person_client.clients.core_client.UWPersonClient._map_person')
    def test_get_person_by_uwregid(self, mock_map_person):
        client = self.get_mock_person_client()
        # person exists
        mock_person = MagicMock()
        mock_regid = 'test',
        client.DB.session.query.return_value.filter.return_value.first = \
            MagicMock(return_value=mock_person)

        return_value = client.get_person_by_uwregid(mock_regid, arg1='arg1')
        # assertions
        client.DB.session.query.assert_called_once_with(
            client.DB.HistoricalPerson)
        client.DB.session.query.return_value.filter.assert_called_once_with(
            client.DB.HistoricalPerson.prior_uwregid == mock_regid)
        client.DB.session.query.return_value.filter.return_value.first.\
            assert_called_once()
        self.assertEqual(
            return_value, mock_map_person(mock_person, arg1='arg1'))

        # no person found
        client.DB.session.query.return_value.filter.return_value.first = \
            MagicMock(return_value=None)
        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_uwregid(mock_regid)

    @patch('uw_person_client.clients.core_client.UWPersonClient._map_person')
    def test_get_person_by_student_number(self, mock_map_person):
        client = self.get_mock_person_client()
        # person exists
        mock_person = MagicMock()
        mock_student_number = 'test',
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.one_or_none = MagicMock(return_value=mock_person)

        return_value = client.get_person_by_student_number(
            mock_student_number, arg1='arg1')
        # assertions
        client.DB.session.query.assert_called_once_with(
            client.DB.Person)
        client.DB.session.query.return_value.join.assert_called_once_with(
            client.DB.Student)
        client.DB.session.query.return_value.join.return_value.filter.\
            assert_called_once_with(
                client.DB.Student.student_number == mock_student_number)
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.one_or_none.assert_called_once()
        self.assertEqual(
            return_value, mock_map_person(mock_person, arg1='arg1'))

        # no person found
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.one_or_none = MagicMock(return_value=None)
        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_student_number(mock_student_number)

    @patch('uw_person_client.clients.core_client.UWPersonClient._map_person')
    def test_get_person_by_system_key(self, mock_map_person):
        client = self.get_mock_person_client()
        # person exists
        mock_person = MagicMock()
        mock_system_key = 'test',
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.one_or_none = MagicMock(return_value=mock_person)

        return_value = client.get_person_by_system_key(
            mock_system_key, arg1='arg1')
        # assertions
        client.DB.session.query.assert_called_once_with(
            client.DB.Person)
        client.DB.session.query.return_value.join.assert_called_once_with(
            client.DB.Student)
        client.DB.session.query.return_value.join.return_value.filter.\
            assert_called_once_with(
                client.DB.Student.system_key == mock_system_key)
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.one_or_none.assert_called_once()
        self.assertEqual(
            return_value, mock_map_person(mock_person, arg1='arg1'))

        # no person found
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.one_or_none = MagicMock(return_value=None)
        with self.assertRaises(PersonNotFoundException):
            client.get_person_by_system_key(mock_system_key)

    @patch('uw_person_client.clients.core_client.UWPersonClient._map_person')
    def test_get_persons(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.all = \
            MagicMock(return_value=[mock_person1, mock_person2])
        return_value = client.get_persons()
        # assertions
        client.DB.session.query.assert_called_once_with(client.DB.Person)
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    @patch('uw_person_client.clients.core_client.UWPDS')
    def test_get_registered_students(self, mock_PDS, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.all=MagicMock(
            return_value=[mock_person1, mock_person2])
        return_value = client.get_registered_students()
        # assertions
        client.DB.session.query.assert_called_once_with(client.DB.Person)
        client.DB.session.query.return_value.join.\
            assert_called_once_with(client.DB.Student)
        client.DB.session.query.return_value.join.return_value.filter.\
            assert_called_once_with(
                client.DB.Student.enroll_status_code == '12')
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

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
