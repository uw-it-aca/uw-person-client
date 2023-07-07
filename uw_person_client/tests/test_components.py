# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_person_client.components import AbstractBase


class AbstractBaseTest(TestCase):

    def test_attributes(self):
        ab = AbstractBase()
        ab.property1 = "value1"
        ab.property2 = "value2"
        self.assertEqual(ab.property1, "value1")
        self.assertEqual(ab.property2, "value2")

        with self.assertRaises(AttributeError):
            ab.foobar

    def test_format_term_desc(self):
        self.assertEqual(Term.format_term_desc(None), None)
        self.assertEqual(Term.format_term_desc(20201), "Winter 2020")
        self.assertEqual(Term.format_term_desc("20213"), "Summer 2021")
