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

from gerrit_cli import gerrit
import unittest


class testParser(unittest.TestCase):
    def setUp(self):
        super(testParser, self).setUp()

    def tearDown(self):
        super(testParser, self).tearDown()

    def testGlobalArgs0(self):
        self.assertRaises(SystemExit, gerrit.parse_arguments, [])

    def testGlobalArgs1(self):
        args = gerrit.parse_arguments(['ls'])

        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'review.openstack.org')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.verbose, None)
        self.assertEqual(args.output_format, 'TABLE')

    def testGlobalArgs2(self):
        args = gerrit.parse_arguments(['-v', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'review.openstack.org')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.verbose, 1)
        self.assertEqual(args.output_format, 'TABLE')

        args = gerrit.parse_arguments(['-vv', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'review.openstack.org')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.verbose, 2)
        self.assertEqual(args.output_format, 'TABLE')

        args = gerrit.parse_arguments(['-vvv', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'review.openstack.org')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.verbose, 3)
        self.assertEqual(args.output_format, 'TABLE')

    def testGlobalArgs3(self):
        args = gerrit.parse_arguments(['--dry-run', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, True)
        self.assertEqual(args.host, 'review.openstack.org')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.output_format, 'TABLE')

    def testGlobalArgs4(self):
        args = gerrit.parse_arguments(['--host', 'abc.def.ghi', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'abc.def.ghi')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.output_format, 'TABLE')

    def testGlobalArgs5(self):
        args = gerrit.parse_arguments(['--host', 'abc.def.ghi',
                                       '--port', '200', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, '~/.gerrit-cli/gerrit-cli.json')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'abc.def.ghi')
        self.assertEqual(args.port, '200')
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.output_format, 'TABLE')

    def testGlobalArgs6(self):
        args = gerrit.parse_arguments(['--config-file', 'xyz', 'ls'])
        self.assertIsNotNone(args)
        self.assertEqual(args.config_file, 'xyz')
        self.assertEqual(args.dry_run, False)
        self.assertEqual(args.host, 'review.openstack.org')
        self.assertEqual(args.port, 29418)
        self.assertEqual(args.query, [])
        self.assertIsNone(args.show)
        self.assertEqual(args.subparser_name, 'ls')
        self.assertEqual(args.output_format, 'TABLE')

    def testGlobalArgs7(self):
        self.assertRaises(SystemExit, gerrit.parse_arguments,
                          ['ls', '--output-format', 'xyz'])

    def testGlobalArgs8(self):
        for format in ['TABLE', 'CSV', 'JSON']:
            args = gerrit.parse_arguments(
                ['ls', '--output-format', format, 'xyz'])

            self.assertEqual(args.output_format, format)
            self.assertEqual(args.subparser_name, 'ls')
            self.assertEqual(args.query, ['xyz'])

    def testListSubparser1(self):
        args = gerrit.parse_arguments(['ls', 'abc'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc'])
        self.assertEqual(args.subparser_name, 'ls')

    def testListSubparser2(self):
        args = gerrit.parse_arguments(['ls', 'abc', 'def', 'ghi'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.subparser_name, 'ls')

    def testListSubparser3(self):
        args = gerrit.parse_arguments(['ls', 'abc', 'def', 'ghi',
                                       '--show', 'pqr', 'def', 'ghi:3'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.show, ['pqr', 'def', 'ghi:3'])
        self.assertEqual(args.subparser_name, 'ls')

    def testShowSubparser1(self):
        args = gerrit.parse_arguments(['show', 'abc'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc'])
        self.assertEqual(args.subparser_name, 'show')

    def testShowSubparser2(self):
        args = gerrit.parse_arguments(['show', 'abc', 'def', 'ghi'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.subparser_name, 'show')

    def _testUARSubParser1(self, op):
        self.assertRaises(SystemExit, gerrit.parse_arguments,
                          [op, '--comment', 'abc'])

    def _testUARSubParser2(self, op):
        args = gerrit.parse_arguments([op, 'abc', '--comment', 'pqr'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc'])
        self.assertEqual(args.comment, ['pqr'])
        self.assertEqual(args.subparser_name, op)

    def _testUARSubParser3(self, op):
        args = gerrit.parse_arguments([op, 'abc', 'def', 'ghi',
                                       '--comment', 'pqr'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.comment, ['pqr'])
        self.assertEqual(args.subparser_name, op)

    def _testUARSubParser4(self, op):
        args = gerrit.parse_arguments([op, 'abc', 'def', 'ghi',
                                       '--comment', 'pqr', 'stu', 'vwz'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.comment, ['pqr', 'stu', 'vwz'])
        self.assertEqual(args.subparser_name, op)

    def _testUARSubParser5(self, op):
        for v in ['-2', '-1', '0', '+1', '+2']:
            args = gerrit.parse_arguments([op, 'abc', 'def', 'ghi',
                                           '--comment', 'pqr', 'stu', 'vwz',
                                           '--review', v])
            self.assertIsNotNone(args)
            self.assertEqual(args.query, ['abc', 'def', 'ghi'])
            self.assertEqual(args.comment, ['pqr', 'stu', 'vwz'])
            self.assertEqual(args.review, v)
            self.assertEqual(args.subparser_name, op)

    def _testUARSubParser6(self, op):
        for w in ['-1', '0', '+1']:
            args = gerrit.parse_arguments([op, 'abc', 'def', 'ghi',
                                           '--comment', 'pqr', 'stu', 'vwz',
                                           '--workflow', w])
            self.assertIsNotNone(args)
            self.assertEqual(args.query, ['abc', 'def', 'ghi'])
            self.assertEqual(args.comment, ['pqr', 'stu', 'vwz'])
            self.assertEqual(args.workflow, w)
            self.assertEqual(args.subparser_name, op)

    def testUARSubParsers(self):
        for op in ['update', 'abandon', 'restore']:
            self._testUARSubParser1(op)
            self._testUARSubParser2(op)
            self._testUARSubParser3(op)
            self._testUARSubParser4(op)
            self._testUARSubParser5(op)
            self._testUARSubParser6(op)

    def testRecheckSubParser1(self):
        self.assertRaises(SystemExit, gerrit.parse_arguments,
                          ['recheck'])

    def testRecheckSubParser2(self):
        args = gerrit.parse_arguments(['recheck', 'abc'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc'])
        self.assertEqual(args.subparser_name, 'recheck')

    def testRecheckSubParser3(self):
        args = gerrit.parse_arguments(['recheck', 'abc', 'def', 'ghi'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.subparser_name, 'recheck')

    def testRecheckSubParser4(self):
        args = gerrit.parse_arguments(['recheck', 'abc', 'def', 'ghi'])
        self.assertIsNotNone(args)
        self.assertEqual(args.query, ['abc', 'def', 'ghi'])
        self.assertEqual(args.subparser_name, 'recheck')

    def testRecheckSubParser5(self):
        for v in ['-2', '-1', '0', '+1', '+2']:
            args = gerrit.parse_arguments(['recheck', 'abc', 'def', 'ghi',
                                           '--review', v])
            self.assertIsNotNone(args)
            self.assertEqual(args.query, ['abc', 'def', 'ghi'])
            self.assertEqual(args.review, v)
            self.assertEqual(args.subparser_name, 'recheck')

    def testRecheckSubParser6(self):
        for w in ['-1', '0', '+1']:
            args = gerrit.parse_arguments(['recheck', 'abc', 'def', 'ghi',
                                           '--workflow', w])
            self.assertIsNotNone(args)
            self.assertEqual(args.query, ['abc', 'def', 'ghi'])
            self.assertEqual(args.workflow, w)
            self.assertEqual(args.subparser_name, 'recheck')
