# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.orm.exc import NoResultFound
from uwpds_client.databases.uwpds import UWPDS
from uwpds_client.components import Person, Student, Employee, \
    Transcript, Major, Sport, Adviser, Term


DB = UWPDS()


class UWPDSClient():

    """
    Public methods
    """

    def get_person_by_uwnetid(self, uwnetid, student=False, employee=False):
        person = DB.session.query(DB.HistoricalPerson).filter(
            DB.HistoricalPerson.prior_uwnetid == uwnetid).first()
        return self._map_person(
            person, include_student=student, include_employee=employee)

    def get_person_by_uwregid(self, uwregid, student=False, employee=False):
        person = DB.session.query(DB.HistoricalPerson).filter(
            DB.HistoricalPerson.prior_uwregid == uwregid).first()
        return self._map_person(
            person, include_student=student, include_employee=employee)

    """
    Private Methods
    """

    def _map_person(self, sqla_person, include_student=False,
                    include_employee=False):
        person = Person()
        person.uwnetid = sqla_person.uwnetid
        person.uwregid = sqla_person.uwregid
        person.pronouns = sqla_person.pronouns
        person.full_name = sqla_person.full_name
        person.display_name = sqla_person.display_name
        person.first_name = sqla_person.first_name
        person.surname = sqla_person.surname
        person.preferred_first_name = sqla_person.preferred_first_name
        person.preferred_middle_name = \
            sqla_person.preferred_middle_name
        person.preferred_surname = sqla_person.preferred_surname
        person.whitepages_publish = sqla_person.whitepages_publish
        person.active_student = sqla_person._is_active_student
        person.active_employee = sqla_person._is_active_employee

        if include_student is True:
            try:
                student = DB.session.query(DB.Student).filter(
                            DB.Student.person_id == sqla_person.id).one()
                person.student = self._map_student(student)
            except NoResultFound:
                pass

        if include_employee is True:
            try:
                employee = DB.session.query(DB.Employee).filter(
                    DB.Employee.person_id == sqla_person.id).one()
                person.employee = self._map_employee(employee)
            except NoResultFound:
                pass

        return person

    def _map_student(self, sqla_student):
        student = Student()
        student.student_number = sqla_student.student_number
        student.assigned_ethnic_code = \
            sqla_student.assigned_ethnic_code
        student.assigned_ethnic_desc = \
            sqla_student.assigned_ethnic_desc
        student.assigned_ethnic_group_desc = \
            sqla_student.assigned_ethnic_group_desc
        student.birthdate = sqla_student.birthdate
        student.student_email = sqla_student.student_email
        student.external_email = sqla_student.external_email
        student.local_phone_number = sqla_student.local_phone_number
        student.gender = sqla_student.gender
        student.cumulative_gpa = sqla_student.cumulative_gpa
        student.total_credits = sqla_student.total_credits
        student.total_uw_credits = sqla_student.total_uw_credits
        student.campus_code = sqla_student.campus_code
        student.campus_desc = sqla_student.campus_desc
        student.class_code = sqla_student.class_code
        student.class_desc = sqla_student.class_desc
        student.resident_code = sqla_student.resident_code
        student.resident_desc = sqla_student.resident_desc
        student.perm_addr_line1 = sqla_student.perm_addr_line1
        student.perm_addr_line2 = sqla_student.perm_addr_line2
        student.perm_addr_city = sqla_student.perm_addr_city
        student.perm_addr_state = sqla_student.perm_addr_state
        student.perm_addr_5digit_zip = sqla_student.perm_addr_5digit_zip
        student.perm_addr_4digit_zip = sqla_student.perm_addr_4digit_zip
        student.perm_addr_country = sqla_student.perm_addr_country
        student.perm_addr_postal_code = sqla_student.perm_addr_postal_code
        student.registered_in_quarter = sqla_student.registered_in_quarter

        # map majors
        student.majors = []
        for major in sqla_student.major:
            major = self._map_major(major)
            student.majors.append(major)

        # map sports
        student.sports = []
        for sport in sqla_student.sport:
            sport = self._map_sport(sport)
            student.sports.append(sport)

        # map advisers
        student.advisers = []
        for adviser in sqla_student.adviser:
            adviser_person = self._map_person(
                adviser.employee.person, include_employee=True)
            student.advisers.append(adviser_person)

        # map transcripts
        student.transcripts = []
        for transcript in sqla_student.transcript:
            transcript = self._map_transcript(transcript)
            student.transcripts.append(transcript)

        return student

    def _map_employee(self, sqla_employee):
        employee = Employee()
        employee.employee_number = sqla_employee.employee_number
        employee.employee_affiliation_state = \
            sqla_employee.employee_affiliation_state
        employee.email_addresses = sqla_employee.email_addresses
        employee.home_department = sqla_employee.home_department
        employee.primary_title = sqla_employee.title
        employee.primary_department = sqla_employee.department

        if sqla_employee.adviser:
            employee.adviser = self._map_adviser(sqla_employee.adviser)

        return employee

    def _map_adviser(self, sqla_adviser):
        adviser = Adviser()
        adviser.is_dept_adviser = sqla_adviser.is_dept_adviser
        adviser.advising_email = sqla_adviser.advising_email
        adviser.advising_phone_number = \
            sqla_adviser.advising_phone_number
        adviser.advising_program = sqla_adviser.advising_program
        adviser.advising_pronouns = sqla_adviser.advising_pronouns
        adviser.booking_url = sqla_adviser.booking_url
        return adviser

    def _map_sport(self, sqla_sport):
        sport = Sport()
        sport.sport_code = sqla_sport.sport_code
        return sport

    def _map_major(self, sqla_major):
        major = Major()
        major.major_abbr_code = sqla_major.major_abbr_code
        major.major_full_code = sqla_major.major_full_code
        major.major_name = sqla_major.major_name
        major.major_short_name = sqla_major.major_short_name
        return major

    def _map_transcript(self, sqla_transcript):
        transcript = Transcript()
        transcript.tran_term = self._map_term(
            sqla_transcript.tran_term)
        transcript.leave_ends_term = self._map_term(
            sqla_transcript.leave_ends_term)
        transcript.resident = sqla_transcript.resident
        transcript.resident_cat = sqla_transcript.resident_cat
        transcript.veteran = sqla_transcript.veteran
        transcript.veteran_benefit = sqla_transcript.veteran_benefit
        transcript.class_code = sqla_transcript.class_code
        transcript.qtr_grade_points = \
            float(sqla_transcript.qtr_grade_points)
        transcript.qtr_graded_attmp = \
            float(sqla_transcript.qtr_graded_attmp)
        transcript.honors_program = sqla_transcript.honors_program
        transcript.special_program = sqla_transcript.special_program
        transcript.scholarship_type = sqla_transcript.scholarship_type
        transcript.yearly_honor_type = sqla_transcript.yearly_honor_type
        transcript.exemption_code = sqla_transcript.exemption_code
        transcript.grad_status = sqla_transcript.grad_status
        transcript.num_ind_study = sqla_transcript.num_ind_study
        transcript.num_courses = sqla_transcript.num_courses
        transcript.enroll_status = sqla_transcript.enroll_status
        transcript.tenth_day_credits = \
            float(sqla_transcript.tenth_day_credits)
        transcript.tr_en_stat_dt = sqla_transcript.tr_en_stat_dt
        return transcript

    def _map_term(self, sqla_term):
        term = Term()
        term.year = sqla_term.year
        term.quarter = sqla_term.quarter
        return term
