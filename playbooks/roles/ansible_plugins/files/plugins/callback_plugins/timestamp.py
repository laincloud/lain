from datetime import datetime

from ansible.callbacks import display


class CallbackModule(object):
    """Show timestamp and time cost for each task run."""

    def __init__(self):
        self.timestamp = datetime.now()

    def playbook_on_task_start(self, name, is_conditional):
        now = datetime.now()
        display("{} (last task costs {})".format(now, now - self.timestamp))
        self.timestamp = now
