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

from subprocess import PIPE
from subprocess import Popen


class GerritSSH(object):
    def __init__(self, config):
        self.config = config

    def query(self, query, limit=-1,
              current_patch_set=False,
              all_patch_sets=True,
              all_approvals=True,
              show_files=False,
              show_comments=False,
              show_commit_message=False,
              show_dependencies=False,
              show_all_reviewers=False):

        cmd = ['ssh', self.config.get('host'),
               '-p', str(self.config.get('port')),
               'gerrit query', '--format=JSON']

        if current_patch_set:
            cmd.append('--current-patch-set')

        if all_patch_sets:
            cmd.append('--patch-sets')

        if all_approvals:
            cmd.append('--all-approvals')

        if show_files:
            cmd.append('--files')

        if show_comments:
            cmd.append('--comments')

        if show_dependencies:
            cmd.append('--dependencies')

        if show_all_reviewers:
            cmd.append('--all-reviewers')

        for element in query:
            cmd.append(element)

        if limit != -1:
            cmd.append("limit:%s" % limit)

        if not self.config.get('dry-run'):
            try:
                p = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE,
                          close_fds=True)
                stdout, stderr = p.communicate()
                if p.returncode != 0:
                    if stderr and stderr != "":
                        print(stderr)
            except Exception:
                raise
        else:
            print(' '.join(cmd))
            return "", ""

        return stdout, stderr

    def _review(self, commitid, message, review, workflow, extra=None):
        cmd = ['ssh', self.config.get('host'),
               '-p', str(self.config.get('port')),
               'gerrit review']

        m = ' '.join(_m for _m in message)

        if len(m.split(' ')) > 1:
            cmd.append('--message \'%s\'' % m)
        else:
            cmd.append('--message %s' % m)

        if review:
            cmd.append('--code-review')
            cmd.append(review)

        if workflow:
            cmd.append('--workflow')
            cmd.append(workflow)

        if extra:
            cmd.append(extra)

        cmd.append(commitid)

        if not self.config.get('dry-run'):
            try:
                p = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE,
                          close_fds=True)
                stdout, stderr = p.communicate()
                if p.returncode != 0:
                    if stdout and stdout != "":
                        print(stdout)
                    if stderr and stderr != "":
                        print(stderr)
            except Exception:
                raise
        else:
            print(' '.join(cmd))

    def update(self, commitid, message, review, workflow):
        return self._review(commitid, message, review, workflow)

    def abandon(self, commitid, message, review, workflow):
        return self._review(commitid, message, review, workflow, '--abandon')

    def restore(self, commitid, message, review, workflow):
        return self._review(commitid, message, review, workflow, '--restore')
