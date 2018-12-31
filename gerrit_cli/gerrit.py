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

import argparse
import json
import os
import re
import sys

from gerrit_list import gerrit_list
from gerrit_list import gerrit_show
from gerrit_update import gerrit_abandon
from gerrit_update import gerrit_recheck
from gerrit_update import gerrit_restore
from gerrit_update import gerrit_update


def parse_arguments(argv):
    # top level parser
    parser = argparse.ArgumentParser(
        prog='gerrit',
        description='A simple gerrit command line interface')

    # top level arguments

    parser.add_argument('--host', action='store',
                        help='The gerrit host. Default: review.openstack.org')
    parser.add_argument('--port', action='store',
                        default=29418,
                        help='The gerrit port. Default: 29418')
    parser.add_argument('--dry-run', action='store_true',
                        help=('Whether or not to actually execute commands '
                              'that modify a review.'))
    parser.add_argument('--config-file', action='store',
                        help=('The path to the gerrit-cli configuration file '
                              'to use for this session. '
                              '(Default: ~/.gerrit-cli/gerrit-cli.json'),
                        default='~/.gerrit-cli/gerrit-cli.json')

    parser.add_argument('-v', '--verbose', action='count',
                        help=('Provide additional (verbose) debug output.'))

    # subparsers
    subparsers = parser.add_subparsers(dest='subparser_name')
    lsparser = subparsers.add_parser('ls', help='list reviews')
    showparser = subparsers.add_parser('show', help='show review(s)')
    updateparser = subparsers.add_parser('update', help='update review(s)')
    abandonparser = subparsers.add_parser('abandon', help='abandon review(s)')
    restoreparser = subparsers.add_parser('restore', help='restore review(s)')
    recheckparser = subparsers.add_parser('recheck', help='abandon review(s)')

    # subparser definitions
    lsparser.add_argument('query', nargs='*',
                          help=('provide a complete gerrit query to execute, '
                                'or a query defined in the configuration '
                                'file'))

    lsparser.add_argument('--show', nargs='*',
                          help='provide a list of columns to display.')
    _output_formats = ['JSON', 'CSV', 'TABLE']
    lsparser.add_argument('--output-format', action='store', default='TABLE',
                          choices=_output_formats,
                          help=('Select an output format, valid choices are '
                                '%s. Default: TABLE' % _output_formats))

    # show parser
    showparser.add_argument('query', nargs='+',
                            help=('provide a complete gerrit query to '
                                  'execute, or a query defined in the '
                                  'configuration file'))

    # update parser
    updateparser.add_argument('query', nargs='+',
                              help=('provide a complete gerrit query to '
                                    'execute, or a query defined in the '
                                    'configuration file'))

    updateparser.add_argument('--comment', nargs='*',
                              required=True, action='store',
                              help='the comment to add with this update')

    updateparser.add_argument('--review',
                              choices=['-2', '-1', '0', '+1', '+2'],
                              required=False, action='store',
                              help='The review score to assign')

    updateparser.add_argument('--workflow',
                              choices=['-1', '0', '+1'],
                              required=False, action='store',
                              help='The workflow score to assign')

    # abandon parser
    abandonparser.add_argument('query', nargs='+',
                               help=('provide a complete gerrit query to '
                                     'execute, or a query defined in the '
                                     'configuration file'))

    abandonparser.add_argument('--comment', nargs='*',
                               required=True, action='store',
                               help='the comment to add with this update')

    abandonparser.add_argument('--review',
                               choices=['-2', '-1', '0', '+1', '+2'],
                               required=False, action='store',
                               help='The review score to assign')

    abandonparser.add_argument('--workflow', choices=['-1', '0', '+1'],
                               required=False, action='store',
                               help='The workflow score to assign')

    # restore parser
    restoreparser.add_argument('query', nargs='+',
                               help=('provide a complete gerrit query to '
                                     'execute, or a query defined in the '
                                     'configuration file'))

    restoreparser.add_argument('--comment', nargs='*',
                               required=True, action='store',
                               help='the comment to add with this update')

    restoreparser.add_argument('--review',
                               choices=['-2', '-1', '0', '+1', '+2'],
                               required=False, action='store',
                               help='The review score to assign')

    restoreparser.add_argument('--workflow', choices=['-1', '0', '+1'],
                               required=False, action='store',
                               help='The workflow score to assign')

    # recheck parser
    recheckparser.add_argument('query', nargs='+',
                               help=('provide a complete gerrit query to '
                                     'execute, or a query defined in the '
                                     'configuration file'))

    recheckparser.add_argument('--review',
                               choices=['-2', '-1', '0', '+1', '+2'],
                               required=False, action='store',
                               help='The review score to assign')

    recheckparser.add_argument('--workflow', choices=['-1', '0', '+1'],
                               required=False, action='store',
                               help='The workflow score to assign')

    args = parser.parse_args(argv)
    return args


def load_configuration(path):
    with open(os.path.expandvars(os.path.expanduser(path))) as config_file:
        c = ''
        comment = re.compile('^\s*#.*')
        for line in config_file:
            if not comment.match(line):
                c = c + line

        return json.loads(c)


def main():
    args = parse_arguments(sys.argv[1:])

    if args.verbose > 0:
        print('arguments are ' + args)

    config = load_configuration(args.config_file)
    #print(config['host'])

    if args.dry_run:
        config['dry-run'] = True

    #print("wes args " + str(args))
    if args.host:
        config['host'] = args.host

    if args.port:
        config['port'] = args.port

    if args.subparser_name == 'ls':
        gerrit_list(args, config)
    elif args.subparser_name == 'show':
        gerrit_show(args, config)
    elif args.subparser_name == 'update':
        gerrit_update(args, config)
    elif args.subparser_name == 'abandon':
        gerrit_abandon(args, config)
    elif args.subparser_name == 'restore':
        gerrit_restore(args, config)
    elif args.subparser_name == 'recheck':
        gerrit_recheck(args, config)

if __name__ == "__main__":
    main()
