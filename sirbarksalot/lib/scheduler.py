from threading import Timer

"""
Courtesy of chadselph
https://gist.github.com/chadselph/4ff85c8c4f68aa105f4b
"""
class Scheduler(object):
    def __init__(self, sleep_time, function, extra_args):
        self.sleep_time = sleep_time
        self.function = function
        self.extra_args = extra_args
        self._t = None

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        self.function(*self.extra_args)
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None