# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class Person():

    def __init__(self, uwnetid=None, uwregid=None, pronouns=None,
                 full_name=None, display_name=None, first_name=None,
                 surname=None, preferred_first_name=None,
                 preferred_middle_name=None, preferred_surname=None,
                 whitepages_publish=None, active_student=False,
                 active_employee=False):
        """
        :type uwnetid: str, optional
        :param uwnetid: person's uw-net-id
        :type uwregid: str, optional
        :param uwregid: person's uw-net-id
        :type pronouns: str, optional
        :param pronouns: person's pronouns (he/his, she/her, .. etc)
        :type full_name: str, optional
        :param full_name: person's registered name
        :type display_name: str, optional
        :param display_name: person's preferred display name
        :type first_name: str, optional
        :param first_name: person's first name
        :type surname: str, optional
        :param surname: person's last name
        :type preferred_first_name: str, optional
        :param preferred_first_name: person's preferred first name
        :type preferred_middle_name: str, optional
        :param preferred_middle_name: person's preferred middle name
        :type preferred_surname: str, optional
        :param preferred_surname: person's preferred last name
        :type whitepages_publish: boolean, optional
        :param whitepages_publish: whether person is published in uw whitepages
        :type active_student: boolean, optional (default=False)
        :param active_student: does person has an active student affiliation
        :type active_employee: boolean, optional (default=False)
        :param active_employee: does person has an active employee affiliation
        """
        self.uwnetid = uwnetid
        self.uwregid = uwregid
