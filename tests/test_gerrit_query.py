# Copyright 2016 Amrith Kumar
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from gerrit_cli import gerrit_query as gq
from mock import patch
import unittest


class testExpandList(unittest.TestCase):
    def setUp(self):
        self.config = {
            "a": ['a1', 'a2', 'a3'],
            "b": ['b1', 'b2', 'b3']
        }
        self.default = ['d1', 'd2', 'd3']
        super(testExpandList, self).setUp()

    def tearDown(self):
        super(testExpandList, self).tearDown()

    def testExpand1(self):
        self.assertRaises(Exception, gq._expand_list,
                          None, self.config, None)
        self.assertRaises(Exception, gq._expand_list,
                          None, self.config, [])
        self.assertRaises(Exception, gq._expand_list,
                          ['default'], self.config, None)
        self.assertRaises(Exception, gq._expand_list,
                          ['default'], self.config, [])

    def testExpand2(self):
        self.assertEqual(self.default,
                         gq._expand_list(['default'],
                                         self.config,
                                         self.default))

    def testExpand3(self):
        self.assertEqual(['d1', 'd2', 'd3', 'x'],
                         gq._expand_list(['default', 'x'],
                                         self.config,
                                         self.default))

    def testExpand4(self):
        self.assertEqual(['d1', 'd2', 'd3', 'a1', 'a2', 'a3'],
                         gq._expand_list(['default', 'a'],
                                         self.config,
                                         self.default))

    def testExpand5(self):
        self.assertEqual(['a1', 'a2', 'a3', 'b1', 'b2', 'b3'],
                         gq._expand_list(['a', 'b'],
                                         self.config,
                                         self.default))

    def testExpand6(self):
        self.assertEqual(['p'],
                         gq._expand_list(['default'],
                                         {"a": ['a1', 'a2', 'a3'],
                                          "b": ['b1', 'b2', 'b3'],
                                          "default": ['p']},
                                         self.default))

    def testExpand7(self):
        self.assertEqual(['123456'],
                         gq._expand_list(['123456'],
                                         {"a": ['a1', 'a2', 'a3'],
                                          "b": ['b1', 'b2', 'b3'],
                                          "default": ['p']},
                                         self.default))

    def testConstrucQuery1(self):
        self.assertEqual(['owner:self', 'status:open'],
                         gq.construct_query(None, None))

    def testConstrucQuery2(self):
        self.assertEqual(['owner:self', 'status:open'],
                         gq.construct_query([], None))

    def testConstrucQuery3(self):
        self.assertEqual(['owner:self', 'status:open'],
                         gq.construct_query(['default'], None))

    def testConstrucQuery4(self):
        self.assertEqual(['pqr', 'stu'],
                         gq.construct_query(
                             ['default'],
                             {'queries': {'default': ['pqr', 'stu']}}))

    def testConstrucShow1(self):
        self.assertEqual([{'align': 'r', 'colname': 'Number',
                           'length': 0, 'name': 'number'},
                          {'align': 'l', 'colname': 'Project',
                           'length': 0, 'name': 'project'},
                          {'align': 'l', 'colname': 'Owner',
                           'length': 0, 'name': 'owner'},
                          {'align': 'l', 'colname': 'Subject',
                           'length': 80, 'name': 'subject'},
                          {'align': 'r', 'colname': 'Age',
                           'length': 0, 'name': 'age'}],
                         gq.construct_show(None, None))

    def testConstrucShow2(self):
        self.assertEqual([{'align': 'r', 'colname': 'Number',
                           'length': 0, 'name': 'number'},
                          {'align': 'l', 'colname': 'Project',
                           'length': 0, 'name': 'project'},
                          {'align': 'l', 'colname': 'Owner',
                           'length': 0, 'name': 'owner'},
                          {'align': 'l', 'colname': 'Subject',
                           'length': 80, 'name': 'subject'},
                          {'align': 'r', 'colname': 'Age',
                           'length': 0, 'name': 'age'}],
                         gq.construct_show([], None))

    def testConstrucShow3(self):
        self.assertEqual([{'align': 'r', 'colname': 'Number',
                           'length': 0, 'name': 'number'},
                          {'align': 'l', 'colname': 'Project',
                           'length': 0, 'name': 'project'},
                          {'align': 'l', 'colname': 'Owner',
                           'length': 0, 'name': 'owner'},
                          {'align': 'l', 'colname': 'Subject',
                           'length': 80, 'name': 'subject'},
                          {'align': 'r', 'colname': 'Age',
                           'length': 0, 'name': 'age'}],
                         gq.construct_show(['default'], None))

    def testConstrucShow4(self):
        self.assertEqual([{'align': 'l', 'colname': 'Pqr',
                           'length': 80, 'name': 'pqr'},
                          {'align': 'r', 'colname': 'Stu',
                           'length': 9, 'name': 'stu'}],
                         gq.construct_show(
                             ['default'],
                             {'results':
                              {'default': ['pqr:l:80', 'stu:r:9']}}))


class testFormatAge(unittest.TestCase):
    def setUp(self):
        super(testFormatAge, self).setUp()

    def tearDown(self):
        super(testFormatAge, self).tearDown()

    def testFormatting(self):
        self.assertEqual('?', gq._format_age(0))
        self.assertEqual('?', gq._format_age(-2))
        self.assertEqual('1s', gq._format_age(1))
        self.assertEqual('59s', gq._format_age(59))
        self.assertEqual('1m', gq._format_age(60))
        self.assertEqual('1m 1s', gq._format_age(61))
        self.assertEqual('1m 59s', gq._format_age(119))
        self.assertEqual('2m', gq._format_age(120))
        self.assertEqual('2m 1s', gq._format_age(121))
        self.assertEqual('22h 59m', gq._format_age(82799))
        self.assertEqual('23h 59m', gq._format_age(86399))
        self.assertEqual('1d', gq._format_age(86400))
        self.assertEqual('1d 1s', gq._format_age(86401))
        self.assertEqual('6d 23h', gq._format_age(604799))
        self.assertEqual('1w', gq._format_age(604800))
        self.assertEqual('1w 1s', gq._format_age(604801))
        self.assertEqual('1w 59s', gq._format_age(604859))
        self.assertEqual('2w', gq._format_age(1209600))
        self.assertEqual('1w 6d', gq._format_age(1209599))
        self.assertEqual('2w 1s', gq._format_age(1209601))
        self.assertEqual('1y', gq._format_age(31536000))
        self.assertEqual('52w 23h', gq._format_age(31535999))
        self.assertEqual('1y 1s', gq._format_age(31536001))


class testFormatState(unittest.TestCase):
    def setUp(self):
        super(testFormatState, self).setUp()

    def tearDown(self):
        super(testFormatState, self).tearDown()

    def testFormatting(self):
        self.assertEqual('None', gq._format_state({}))


class testFormatColumn(unittest.TestCase):
    def setUp(self):
        super(testFormatColumn, self).setUp()

    def tearDown(self):
        super(testFormatColumn, self).tearDown()

    def testFormat1(self):
        self.assertEqual(200, gq._format_column(0, {'name': 'number',
                                                    'length': 0},
                                                {'number': '200'}))

    def testFormat2(self):
        self.assertEqual('1s', gq._format_column(101, {'name': 'age',
                                                       'length': 0},
                                                 {'lastUpdated': 100}))
        self.assertEqual('1m 1s', gq._format_column(161, {'name': 'age',
                                                          'length': 0},
                                                    {'lastUpdated': 100}))

    def testFormat3(self):
        self.assertEqual('the time has come',
                         gq._format_column(101, {'name': 'subject',
                                                 'length': 0},
                                           {'subject': 'the time has come'}))

    def testFormat4(self):
        self.assertEqual('the time has come',
                         gq._format_column(101, {'name': 'subject',
                                                 'length': 100},
                                           {'subject': 'the time has come'}))

    def testFormat5(self):
        self.assertEqual('the tim...',
                         gq._format_column(101, {'name': 'subject',
                                                 'length': 10},
                                           {'subject': 'the time has come'}))

    def testFormat6(self):
        self.assertEqual('the time    ...',
                         gq._format_column(101, {'name': 'subject',
                                                 'length': 15},
                                           {'subject': 'the time \thas come'}))

    def testFormat7(self):
        self.assertEqual('abc',
                         gq._format_column(101, {'name': 'owner',
                                                 'length': 0},
                                           {'owner': {'name': 'abc',
                                                      'username': 'pqr',
                                                      'email': 'abc@pqr'}}))

    def testFormat8(self):
        self.assertEqual('pqr',
                         gq._format_column(101, {'name': 'owner',
                                                 'length': 0},
                                           {'owner': {'username': 'pqr',
                                                      'email': 'abc@pqr'}}))

    def testFormat9(self):
        self.assertEqual('abc@pqr',
                         gq._format_column(101, {'name': 'owner',
                                                 'length': 0},
                                           {'owner': {'email': 'abc@pqr'}}))

    def testFormat10(self):
        self.assertEqual('12',
                         gq._format_column(101, {'name': 'commitid',
                                                 'length': 0},
                                           {'patchSets': [
                                               {'revision': '11'},
                                               {'revision': '12'}]}))

    def testFormat11(self):
        self.assertEqual('12',
                         gq._format_column(101, {'name': 'patchset',
                                                 'length': 0},
                                           {'patchSets': [
                                               {'number': '11'},
                                               {'number': '12'}]}))

    def testFormat12(self):
        self.assertEqual('abc',
                         gq._format_column(101, {'name': 'foo',
                                                 'length': 0},
                                           {'foo': 'abc',
                                            'patchSets': [
                                                {'number': '11'},
                                                {'number': '12'}]}))


class testProcessResults(unittest.TestCase):
    def setUp(self):
        super(testProcessResults, self).setUp()

    def tearDown(self):
        super(testProcessResults, self).tearDown()

    def testProcessResults1(self):
        results = "\n".join(['{"number": "1"}',
                             '{"rowCount": "1"}'])
        self.assertEqual([{'number': '1'}],
                         gq.process_results(results))

    def testProcessResults2(self):
        results = "\n".join(['{"number": "1"}',
                             '{"number": "2", "pqr": "stu"}',
                             '{"rowCount": "2"}'])
        self.assertEqual([{'number': '1'},
                          {"number": "2", "pqr": "stu"}],
                         gq.process_results(results))

    def testProcessResults3(self):
        results = "\n".join(['{"number": "1"}',
                             '{"number": "2", "pqr": "stu"}',
                             '{"rowCount": "3"}'])
        self.assertRaises(Exception, gq.process_results, results)


class testGenerateOutput(unittest.TestCase):
    def setUp(self):
        self.output = '\n'.join(
            ['{"number": "1", "project": "abc", "owner": {"name": "abc", \
            "username": "pqr", "email": "abc@pqr"}, "subject": "subject1", \
            "lastUpdated": "199"}',
             '{"number": "2", "project": "def", "owner": {"name": "def", \
             "username": "def", "email": "abc@pqr"}, "subject": "subject2", \
             "lastUpdated": "199"}',
             '{"number": "3", "project": "ghi", "owner": {"name": "ghi", \
             "username": "pqr", "email": "abc@pqr"}, "subject": "subject3", \
             "lastUpdated": "198"}',
             '{"rowCount": "3"}'])

        super(testGenerateOutput, self).setUp()

    def tearDown(self):
        super(testGenerateOutput, self).tearDown()

    def testGenerateOutput1(self):
        with patch('time.time', return_value=200):
            self.assertEqual(([[1], [2], [3]],
                              [{'length': 0, 'name': 'number', 'align': 'r',
                                'colname': 'Number'}, ]),
                             gq.generate_output(self.output,
                                                [{"align": "r",
                                                  "colname": "Number",
                                                  "length": 0,
                                                  "name": "number"}]))

    def testGenerateOutput2(self):
        with patch('time.time', return_value=200):
            self.assertEqual(
                ([[1, '1s'], [2, '1s'], [3, '2s']],
                 [{'length': 0, 'name': 'number', 'align': 'r',
                   'colname': 'Number'},
                  {'align': 'r', 'colname': 'Age', 'length': 0,
                   'name': 'age'}]),
                gq.generate_output(self.output,
                                   [{"align": "r",
                                     "colname": "Number",
                                     "length": 0,
                                     "name": "number"},
                                    {"align": "r",
                                     "colname": "Age",
                                     "length": 0,
                                     "name": "age"}]))
