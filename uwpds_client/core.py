# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uwpds_client.databases.postgres import Postgres
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound


DB = Postgres()
Person = DB.Base.classes.person
Student = DB.Base.classes.student
Employee = DB.Base.classes.employee


class PersonClient():

    def _get_person_dict(self, uwnetid=None, uwregid=None, student=False,
                         employee=False):
        person = DB.session.query(Person).filter(
            or_(Person.uwnetid == uwnetid,
                Person.uwregid == uwregid)).one()
        person_dict = {}
        person_dict["uwnetid"] = person.uwnetid
        person_dict["uwregid"] = person.uwregid
        person_dict["pronouns"] = person.pronouns
        person_dict["full_name"] = person.full_name
        person_dict["display_name"] = person.display_name
        person_dict["first_name"] = person.first_name
        person_dict["surname"] = person.surname
        person_dict["preferred_first_name"] = person.preferred_first_name
        person_dict["preferred_middle_name"] = person.preferred_middle_name
        person_dict["preferred_surname"] = person.preferred_surname
        person_dict["whitepages_publish"] = person.whitepages_publish
        person_dict["active_student"] = person._is_active_student
        person_dict["active_employee"] = person._is_active_employee

        if student is True:
            try:
                student_client = StudentClient()
                person_dict["student"] = \
                    student_client._get_student_dict(person)
            except NoResultFound:
                pass

        if employee is True:
            try:
                employee_client = EmployeeClient()
                person_dict["employee"] = \
                    employee_client._get_employee_dict(person)
            except NoResultFound:
                pass

        return person_dict

    def get_person_by_uwnetid(self, uwnetid, student=False, employee=False):
        return self._get_person_dict(
            uwnetid=uwnetid, student=student, employee=employee)

    def get_person_by_uwregid(self, uwregid, student=False, employee=False):
        return self._get_person_dict(
            uwregid=uwregid, student=student, employee=employee)


class StudentClient():

    def _get_student_dict(self, person):
        student = DB.session.query(Student).filter(
            Student.person_id == person.id).one()
        student_dict = {}
        student_dict["student_number"] = student.student_number
        student_dict["assigned_ethnic_code"] = student.assigned_ethnic_code
        student_dict["assigned_ethnic_desc"] = student.assigned_ethnic_desc
        student_dict["assigned_ethnic_group_desc"] = \
            student.assigned_ethnic_group_desc
        student_dict["birthdate"] = student.birthdate
        student_dict["student_email"] = student.student_email
        student_dict["external_email"] = student.external_email
        student_dict["local_phone_number"] = student.local_phone_number
        student_dict["gender"] = student.gender
        student_dict["gpa"] = student.gpa
        student_dict["total_credits"] = student.total_credits
        student_dict["total_uw_credits"] = student.total_uw_credits
        student_dict["campus_code"] = student.campus_code
        student_dict["campus_desc"] = student.campus_desc
        student_dict["class_code"] = student.class_code
        student_dict["class_desc"] = student.class_desc
        student_dict["honors_program_code"] = student.honors_program_code
        student_dict["honors_program_ind"] = student.honors_program_ind
        student_dict["resident_code"] = student.resident_code
        student_dict["resident_desc"] = student.resident_desc
        student_dict["perm_addr_line1"] = student.perm_addr_line1
        student_dict["perm_addr_line2"] = student.perm_addr_line2
        student_dict["perm_addr_city"] = student.perm_addr_city
        student_dict["perm_addr_state"] = student.perm_addr_state
        student_dict["perm_addr_5digit_zip"] = student.perm_addr_5digit_zip
        student_dict["perm_addr_4digit_zip"] = student.perm_addr_4digit_zip
        student_dict["perm_addr_country"] = student.perm_addr_country
        student_dict["perm_addr_postal_code"] = student.perm_addr_postal_code
        student_dict["registered_in_quarter"] = student.registered_in_quarter
        return student_dict


class EmployeeClient():

    def _get_employee_dict(self, person):
        employee = DB.session.query(Employee).filter(
            Employee.person_id == person.id).one()
        employee_dict = {}
        employee_dict["employee_number"] = employee.employee_number
        employee_dict["employee_affiliation_state"] = \
            employee.employee_affiliation_state
        employee_dict["email_addresses"] = employee.email_addresses
        employee_dict["home_department"] = employee.home_department
        employee_dict["primary_title"] = employee.title
        employee_dict["primary_department"] = employee.department
        return employee_dict
