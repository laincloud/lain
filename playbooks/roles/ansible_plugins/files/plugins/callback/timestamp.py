from datetime import datetime

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """Show timestamp and time cost for each task run."""

    def __init__(self):
        super(CallbackModule, self).__init__()

        self.timestamp = datetime.now()

    def playbook_on_task_start(self, name, is_conditional):
        now = datetime.now()
        self._display.display("{} (last task costs {})".format(now, now - self.timestamp))
        self.timestamp = now
