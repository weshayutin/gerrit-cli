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

import json
from prettytable import PrettyTable

from gerrit_query import construct_query
from gerrit_query import construct_show
from gerrit_query import generate_output
from gerrit_query import process_results
from gerrit_ssh import GerritSSH


def _generate_list(args, config):
    query = construct_query(args.query, config)
    show = construct_show(args.show, config)
    print("ls config " + str(config))

    session = GerritSSH(config)
    out, err = session.query(query, current_patch_set=True)

    return generate_output(out, show)


def gerrit_list(args, config):
    output, show = _generate_list(args, config)

    if args.output_format == 'TABLE':
        table = PrettyTable(
            [f.get('colname') for f in show],
            sortby=show[0].get('colname'))

        for f in show:
            table.align[f.get('colname')] = f.get('align')

        for row in output:
            table.add_row(row)

        print(table)
    elif args.output_format == 'CSV':
        print(','.join(f.get('colname') for f in show))
        for row in output:
            print(','.join(('"%s"' % str(c).replace('"', '"""')) for c in row))
    elif args.output_format == 'JSON':
        o = []
        for row in output:
            e = {}
            for colix in range(0, len(show)):
                e[show[colix].get('name')] = row[colix]
            o.append(e)

        print(o)


def gerrit_show(args, config):
    query = construct_query(args.query, config)
    session = GerritSSH(config)

    out, err = session.query(query, current_patch_set=True)
    reviews = process_results(out)

    for row in reviews:
        print(json.dumps(row, indent=2))
