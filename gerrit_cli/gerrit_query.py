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

#
# gerrit_query:
#
# given the query from the command line, construct the expanded query
# based on user defined queries (expanding user defined queries).
#
# given a show list (columns to show), expand the list based on user defined
# show lists in the configuration.
#

import json
import time


def _get_item(item, configdict):
    # print("_get_item(%s), %s" % (item, type(item)))
    if configdict and (len(configdict) > 0 and
                       configdict.get(item) is not None):
        _o = configdict.get(item)
    else:
        _o = [item]

    if type(_o) != list:
        raise Exception("the item %s resolves to a non-list %s" %
                        (item, _o))

    return _o


def _get_default(configdict, default):
    if configdict and (configdict.get('default')
                       and len(configdict.get('default')) > 0):
        return configdict.get('default')
    elif default and len(default) > 0:
        return default
    else:
        raise Exception("no default provided for expansion")


def _expand_list(inlist, configdict, default):
    # print("_expand_list(%s)" % inlist)
    # given an input list (inlist), expand each item in the list
    # and generate a list of strings constituting a query
    if len(inlist) == 0:
        _o = _get_default(configdict, default)

        return _o

    _o = inlist
    inlist = None

    while _o != inlist:
        # print(">_o = %s, inlist = %s" % (_o, inlist))
        inlist = _o
        _o = []

        for element in inlist:
            if element == "default":
                _e = _get_default(configdict, default)
            else:
                _e = _get_item(element, configdict)

            # print("_e = %s" % _e)
            for e in _e:
                _o.append(e)

        # print("<_o = %s, inlist = %s" % (_o, inlist))

    return _o


def _format_state(cps):
    approvals = cps.get('approvals', None)
    if approvals is None:
        return "None"

    _code_review = [0, 0, 0, 0, 0]
    _verified = [0, 0, 0, 0, 0]
    _workflow = [0, 0, 0]

    for approval in approvals:
        if approval.get('type') == 'Code-Review':
            _code_review[int(approval.get('value')) + 2] += 1
        elif approval.get('type') == 'Workflow':
            _workflow[int(approval.get('value')) + 1] += 1
        elif approval.get('type') == 'Verified':
            _verified[int(approval.get('value')) + 2] += 1
        elif approval.get('type') == 'Rollcall-Vote':
            pass
        else:
            raise Exception("Unknown approval type %s" % approval.get('type'))

    _cr = str(_code_review).replace(' ', '')
    _wf = str(_workflow).replace(' ', '')
    _ve = str(_verified).replace(' ', '')

    return "R:%s W:%s V:%s" % (_cr, _wf, _ve)


def _format_age(age_s):
    age = ""
    steps = ((3600 * 24 * 365, "y"), (3600 * 24 * 7, "w"),
             (3600 * 24, "d"), (3600, "h"),
             (60, "m"), (0, "s"))

    components = []

    if age_s <= 0:
        return '?'

    for step in steps:
        if age_s > 0 and age_s >= step[0]:
            if step[0] > 0:
                s = int(age_s / step[0])
                components.append("%s%s" % (s, step[1]))
                age_s = (age_s - s * step[0])
            else:
                components.append("%s%s" % (int(age_s), step[1]))
                age_s = 0

    if len(components) >= 2:
        age = ' '.join(s for s in components[0:2])
    else:
        age = ' '.join(s for s in components)

    return age


def _format_column(now, column, review):
    field = column.get('name')
    length = column.get('length')

    if field == 'number':
        return int(review.get(field))

    if field == 'age':
        data = _format_age(now - int(review.get('lastUpdated')))
    elif field == 'state':
        data = _format_state(review.get('currentPatchSet'))
    elif field == 'subject':
        data = review.get('subject').replace('\t', '   ')
    elif field == 'owner':
        o = review.get('owner')
        data = o.get('name', o.get('username', o.get('email')))
    elif field == 'commitid':
        data = review.get('patchSets')[-1].get('revision')
    elif field == 'patchset':
        data = review.get('patchSets')[-1].get('number')
    else:
        data = review.get(field)

    if length > 0 and len(data) > length:
        data = data[0:length - 3] + "..."

    return data


def process_results(o):
    output = []
    rows = 0
    rowcount = 0

    for line in o.split("\n"):
        if line != "":
            review = json.loads(line)
            if review.get('number', None) is not None:
                rows += 1
                output.append(review)
            elif review.get('rowCount') is not None:
                rowcount = int(review.get('rowCount'))

    if rows != rowcount:
        raise Exception("mismatch between expected and found rows.")

    return output


def construct_query(inlist, config):
    _i = ['default'] if inlist is None or len(inlist) == 0 else inlist

    return _expand_list(_i, config.get('queries') if config else None,
                        ['owner:self', 'status:open'])


def construct_show(inlist, config):
    _i = ['default'] if inlist is None or len(inlist) == 0 else inlist

    expanded_list = _expand_list(_i, config.get('results') if config else None,
                                 ["number:r", "project:l", "owner:l",
                                  "subject:l:80", "age:r"])
    show_list = []
    for element in expanded_list:
        pieces = element.split(':')
        name = pieces[0]
        align = pieces[1] if len(pieces) > 1 and pieces[1] != '' else 'r'
        length = int(pieces[2] if len(pieces) > 2 and pieces[2] != '' else 0)

        show_list.append({"name": name, "colname": name.capitalize(),
                          "align": align, "length": length})

    return show_list


def generate_output(o, show):
    reviews = process_results(o)
    now = time.time()

    data = []

    for review in reviews:
        row = []

        for column in show:
            row.append(_format_column(now, column, review))

        data.append(row)

    return data, show
