from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import datetime
import time
import json

from ansible.plugins.callback import CallbackBase

FIELDS = ['command',
          'start',
          'end',
          'msg',
          'stdout',
          'stderr',
          'results',
          'failed', ]

class CallbackModule(CallbackBase):

    def __init__(self):
        super(CallbackModule, self).__init__()

        self.task_times = {}
        self.current_time = None


    def humanize(self, data):
        if type(data) == dict:
            for field in FIELDS:
                if field in data.keys() and data[field]:
                    output = json.dumps(data[field], indent=2, sort_keys=True)
                    if type(output) != list:
                        (self._display.display("\n{0}:\n{1}".format(
                            field, output.replace("\\n","\n")), log_only=False))
                    else:
                        print(u'\n{0}:\n{1}'.format(field, data[field]))


    def v2_on_any(self, *args, **kwargs):
        pass

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.humanize(result._result)

    def v2_runner_on_ok(self, result):
        self.humanize(result._result)

    def v2_runner_on_skipped(self, result):
        pass

    def v2_runner_on_unreachable(self, result):
        self.humanize(result._result)

    def v2_runner_on_no_hosts(self, task):
        pass

    def v2_runner_on_async_poll(self, result):
        self.humanize(result._result)

    def v2_runner_on_async_ok(self, host, result):
        self.humanize(result._result)

    def v2_runner_on_async_failed(self, result):
        self.humanize(result._result)

    def v2_playbook_on_notify(self, result, handler):
        pass

    def v2_playbook_on_no_hosts_matched(self):
        pass

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        pass

    def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                   encrypt=None, confirm=False, salt_size=None,
                                   salt=None, default=None):
        pass

    def v2_playbook_on_setup(self):
        pass

    def v2_playbook_on_import_for_host(self, result, imported_file):
        pass

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        pass

    def v2_playbook_on_play_start(self, play):
        if self.current_time is not None:
            self.task_times[self.current_time] = time.time() - self.task_times[self.current_time]
        self.current_time = play
        self.task_times[self.current_time] = time.time()

    def v2_playbook_on_stats(self, task_times):
        if self.current_time is not None:
            self.task_times[self.current_time] = time.time() - self.task_times[self.current_time]
        results = sorted(
            self.task_times.items(),
            key=lambda value: value[1],
            reverse=True,
        )
        results = results[:10]
        for name, elapsed in results:
            print(
                "{0:-<65}{1:->10}".format(
                    '{0} '.format(name),
                    ' {0:.02f}s'.format(elapsed),
                )
            )
        total_seconds = sum([x[1] for x in self.task_times.items()])
        print("\nFinished: {0}, {1} total tasks.  {2} elapsed. \n".format(
            time.asctime(),
            len(self.task_times.items()),
            datetime.timedelta(seconds=(int(total_seconds)))
            )
        )

    def v2_on_file_diff(self, result):
        pass

    def v2_playbook_on_item_ok(self, result):
        pass

    def v2_playbook_on_item_failed(self, result):
        pass

    def v2_playbook_on_item_skipped(self, result):
        pass

    def v2_playbook_on_include(self, included_file):
        pass

    def v2_playbook_item_on_ok(self, result):
        pass

    def v2_playbook_item_on_failed(self, result):
        pass

    def v2_playbook_item_on_skipped(self, result):
        pass




