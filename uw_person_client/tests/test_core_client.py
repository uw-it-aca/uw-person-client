# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from unittest.mock import patch, MagicMock
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
    def test_get_registered_students(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.join.return_value.filter.\
            return_value.all = MagicMock(
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
    def test_get_active_students(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.filter.return_value.\
            all = MagicMock(return_value=[mock_person1, mock_person2])
        return_value = client.get_active_students()
        # assertions
        client.DB.session.query.assert_called_once_with(client.DB.Person)
        client.DB.session.query.return_value.filter.assert_called_once_with(
            client.DB.Person._is_active_student == True)  # noqa
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    def test_get_active_employees(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.filter.return_value.\
            all = MagicMock(return_value=[mock_person1, mock_person2])
        return_value = client.get_active_employees()
        # assertions
        client.DB.session.query.assert_called_once_with(client.DB.Person)
        client.DB.session.query.return_value.filter.assert_called_once_with(
            client.DB.Person._is_active_employee == True)  # noqa
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    def test_get_advisers(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.all = MagicMock(
                return_value=[mock_person1, mock_person2])
        return_value = client.get_advisers()
        # assertions
        client.DB.session.query.assert_called_once_with(client.DB.Person)
        client.DB.session.query.return_value.join.assert_called_once_with(
            client.DB.Employee)
        client.DB.session.query.return_value.join.return_value.join.\
            assert_called_once_with(client.DB.Adviser)
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    def test_get_advisers_with_program(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.filter.return_value.all = MagicMock(
                return_value=[mock_person1, mock_person2])
        return_value = client.get_advisers(advising_program='test')
        # assertions
        client.DB.session.query.assert_called_once_with(client.DB.Person)
        client.DB.session.query.return_value.join.assert_called_once_with(
            client.DB.Employee)
        client.DB.session.query.return_value.join.return_value.join.\
            assert_called_once_with(client.DB.Adviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.filter.assert_called_once_with(
                client.DB.Person._is_active_employee == True)  # noqa
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    def test_get_persons_by_adviser_netid_not_found(self):
        client = self.get_mock_person_client()
        client.DB.session.query = MagicMock(side_effect=NoResultFound)
        with self.assertRaises(AdviserNotFoundException):
            client.get_persons_by_adviser_netid('test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    def test_get_persons_by_adviser_netid(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_adviser = MagicMock()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        mock_netid = 'netid'
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.filter.return_value.one = MagicMock(
                return_value=mock_adviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.join.return_value.filter.return_value.all = MagicMock(
                return_value=[mock_person1, mock_person2])
        return_value = client.get_persons_by_adviser_netid(mock_netid)
        # assertions
        client.DB.session.query.assert_any_call(client.DB.Person)
        client.DB.session.query.assert_any_call(client.DB.Adviser)
        client.DB.session.query.return_value.join.assert_any_call(
            client.DB.Employee)
        client.DB.session.query.return_value.join.assert_any_call(
            client.DB.Student)
        client.DB.session.query.return_value.join.return_value.join.\
            assert_any_call(client.DB.Person)
        client.DB.session.query.return_value.join.return_value.join.\
            assert_any_call(client.DB.StudentToAdviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.filter.assert_called_once_with(
                client.DB.Person.uwnetid == mock_netid)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.join.assert_called_once_with(
                client.DB.Adviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.join.return_value.filter.assert_called_once_with(
                client.DB.Adviser.id == mock_adviser.id)
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    def test_get_persons_by_adviser_regid_not_found(self):
        client = self.get_mock_person_client()
        client.DB.session.query = MagicMock(side_effect=NoResultFound)
        with self.assertRaises(AdviserNotFoundException):
            client.get_persons_by_adviser_regid('test')

    @patch.object(UWPersonClient, '_map_person', return_value=None)
    def test_get_persons_by_adviser_regid(self, mock_map_person):
        client = self.get_mock_person_client()
        mock_adviser = MagicMock()
        mock_person1, mock_person2 = MagicMock(), MagicMock()
        mock_regid = 'regid'
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.filter.return_value.one = MagicMock(
                return_value=mock_adviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.join.return_value.filter.return_value.all = MagicMock(
                return_value=[mock_person1, mock_person2])
        return_value = client.get_persons_by_adviser_regid(mock_regid)
        # assertions
        client.DB.session.query.assert_any_call(client.DB.Person)
        client.DB.session.query.assert_any_call(client.DB.Adviser)
        client.DB.session.query.return_value.join.assert_any_call(
            client.DB.Employee)
        client.DB.session.query.return_value.join.assert_any_call(
            client.DB.Student)
        client.DB.session.query.return_value.join.return_value.join.\
            assert_any_call(client.DB.Person)
        client.DB.session.query.return_value.join.return_value.join.\
            assert_any_call(client.DB.StudentToAdviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.filter.assert_called_once_with(
                client.DB.Person.uwregid == mock_regid)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.join.assert_called_once_with(
                client.DB.Adviser)
        client.DB.session.query.return_value.join.return_value.join.\
            return_value.join.return_value.filter.assert_called_once_with(
                client.DB.Adviser.id == mock_adviser.id)
        self.assertEqual(return_value,
                         [mock_map_person(mock_person1),
                          mock_map_person(mock_person2)])

    def test_map_person(self):
        client = self.get_mock_person_client()
        mock_person1 = MagicMock()
        return_value = client._map_person(mock_person1)
        self.assertIsInstance(return_value, Person)
