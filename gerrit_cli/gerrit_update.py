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

from gerrit_query import construct_query
from gerrit_query import construct_show
from gerrit_query import generate_output

from gerrit_ssh import GerritSSH


def _do_change(args, config, op):
    show_list = ['number', 'subject:l:70', 'commitid', 'patchset']

    query = construct_query(args.query, config)
    show = construct_show(show_list, config)

    session = GerritSSH(config)
    out, err = session.query(query, current_patch_set=True)
    reviews, _ = generate_output(out, show)

    for review in reviews:
        number = review[0]
        subject = review[1]
        commitid = review[2]
        patchset = review[3]

        print("%s review %s,%s [%s]" % (op, number, patchset, subject))
        if op == "update":
            session.update(commitid, args.comment, args.review, args.workflow)
        elif op == "recheck":
            session.update(commitid, ['recheck'], args.review, args.workflow)
        elif op == "abandon":
            session.abandon(commitid, args.comment, args.review, args.workflow)
        elif op == "restore":
            session.restore(commitid, args.comment, args.review, args.workflow)
        else:
            raise Exception("unknown operation")


def gerrit_update(args, config):
    _do_change(args, config, "update")


def gerrit_recheck(args, config):
    _do_change(args, config, "recheck")


def gerrit_abandon(args, config):
    _do_change(args, config, "abandon")


def gerrit_restore(args, config):
    _do_change(args, config, "restore")
