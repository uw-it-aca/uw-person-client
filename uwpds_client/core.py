# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.orm.exc import NoResultFound
from uwpds_client.databases.uwpds import UWPDS


DB = UWPDS()


class UWPDSClient():

    """
    Public methods
    """

    def get_person_by_uwnetid(self, uwnetid, student=False, employee=False):
        person = DB.session.query(DB.Person).filter(
            DB.Person.uwnetid == uwnetid).one()
        return self._map_person_dict(
            person, include_student=student, include_employee=employee)

    def get_person_by_uwregid(self, uwregid, student=False, employee=False):
        person = DB.session.query(DB.Person).filter(
            DB.Person.uwregid == uwregid).one()
        return self._map_person_dict(
            person, include_student=student, include_employee=employee)

    """
    Private Methods
    """

    def _map_person_dict(self, person, include_student=False,
                         include_employee=False):
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

        if include_student is True:
            try:
                student = DB.session.query(DB.Student).filter(
                            DB.Student.person_id == person.id).one()
                person_dict["student"] = \
                    self._map_student_dict(student)
            except NoResultFound:
                pass

        if include_employee is True:
            try:
                employee = DB.session.query(DB.Employee).filter(
                    DB.Employee.person_id == person.id).one()
                person_dict["employee"] = \
                    self._map_employee_dict(employee)
            except NoResultFound:
                pass

        return person_dict

    def _map_student_dict(self, student):
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
        student_dict["cumulative_gpa"] = student.cumulative_gpa
        student_dict["total_credits"] = student.total_credits
        student_dict["total_uw_credits"] = student.total_uw_credits
        student_dict["campus_code"] = student.campus_code
        student_dict["campus_desc"] = student.campus_desc
        student_dict["class_code"] = student.class_code
        student_dict["class_desc"] = student.class_desc
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

        # map majors
        student_dict["majors"] = []
        for major in student.major:
            major_dict = self._map_major(major)
            student_dict["majors"].append(major_dict)

        # map sports
        student_dict["sports"] = []
        for sport in student.sport:
            sport_dict = self._map_sport(sport)
            student_dict["sports"].append(sport_dict)

        # map advisers
        student_dict["advisers"] = []
        for adviser in student.adviser:
            adviser_person_dict = self._map_person_dict(
                adviser.employee.person, include_employee=True)
            student_dict["advisers"].append(adviser_person_dict)

        # map transcripts
        student_dict["transcripts"] = []
        for transcript in student.transcript:
            transcript_dict = self._map_transcript(transcript)
            student_dict["transcripts"].append(transcript_dict)

        return student_dict

    def _map_employee_dict(self, employee):
        employee_dict = {}
        employee_dict["employee_number"] = employee.employee_number
        employee_dict["employee_affiliation_state"] = \
            employee.employee_affiliation_state
        employee_dict["email_addresses"] = employee.email_addresses
        employee_dict["home_department"] = employee.home_department
        employee_dict["primary_title"] = employee.title
        employee_dict["primary_department"] = employee.department

        if employee.adviser:
            employee_dict["adviser"] = self._map_adviser(employee.adviser)

        return employee_dict

    def _map_adviser(self, adviser):
        adviser_dict = {}
        adviser_dict["is_dept_adviser"] = adviser.is_dept_adviser
        adviser_dict["advising_email"] = adviser.advising_email
        adviser_dict["advising_phone_number"] = \
            adviser.advising_phone_number
        adviser_dict["advising_program"] = adviser.advising_program
        adviser_dict["advising_pronouns"] = adviser.advising_pronouns
        adviser_dict["booking_url"] = adviser.booking_url
        return adviser_dict

    def _map_sport(self, sport):
        sport_dict = {}
        sport_dict["sport_code"] = sport.sport_code
        return sport_dict

    def _map_major(self, major):
        major_dict = {}
        major_dict["major_abbr_code"] = major.major_abbr_code
        major_dict["major_full_code"] = major.major_full_code
        major_dict["major_name"] = major.major_name
        major_dict["major_short_name"] = major.major_short_name
        return major_dict

    def _map_transcript(self, transcript):
        transcript_dict = {}
        transcript_dict["tran_term"] = self._map_term(
            transcript.tran_term)
        transcript_dict["leave_ends_term"] = self._map_term(
            transcript.leave_ends_term)
        # transcript_dict["tran_net_id"] = transcript.tran_net_id
        transcript_dict["resident"] = transcript.resident
        transcript_dict["resident_cat"] = transcript.resident_cat
        transcript_dict["veteran"] = transcript.veteran
        transcript_dict["veteran_benefit"] = transcript.veteran_benefit
        transcript_dict["class_code"] = transcript.class_code
        transcript_dict["qtr_grade_points"] = \
            float(transcript.qtr_grade_points)
        transcript_dict["qtr_graded_attmp"] = \
            float(transcript.qtr_graded_attmp)
        transcript_dict["honors_program"] = transcript.honors_program
        transcript_dict["special_program"] = transcript.special_program
        transcript_dict["scholarship_type"] = transcript.scholarship_type
        transcript_dict["yearly_honor_type"] = transcript.yearly_honor_type
        transcript_dict["exemption_code"] = transcript.exemption_code
        transcript_dict["grad_status"] = transcript.grad_status
        transcript_dict["num_ind_study"] = transcript.num_ind_study
        transcript_dict["num_courses"] = transcript.num_courses
        transcript_dict["enroll_status"] = transcript.enroll_status
        transcript_dict["tenth_day_credits"] = \
            float(transcript.tenth_day_credits)
        transcript_dict["tr_en_stat_dt"] = transcript.tr_en_stat_dt
        print(transcript_dict)
        return transcript_dict

    def _map_term(self, term):
        term_dict = {}
        term_dict["year"] = term.year
        term_dict["quarter"] = term.quarter
        return term_dict
