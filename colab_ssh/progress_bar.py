# pylint: disable=missing-function-docstring
"""
Progress bar for Jupyter notebook

https://salsa.debian.org/apt-team/python-apt
https://apt-team.pages.debian.net/python-apt/library/index.html
"""

from IPython.core.display import display
import apt
import apt.debfile
import ipywidgets

class NoteProgress(apt.progress.base.InstallProgress, apt.progress.base.AcquireProgress, apt.progress.base.OpProgress):
    """
    Progress bar for Jupyter notebook
    """
    def __init__(self):
        apt.progress.base.InstallProgress.__init__(self)
        self._label = ipywidgets.Label()
        display(self._label)
        self._float_progress = ipywidgets.FloatProgress(
            min=0.0, max=1.0, layout={'border': '1px solid #118800'})
        display(self._float_progress)

    def close(self):
        self._float_progress.close()
        self._label.close()

    def fetch(self, item):
        self._label.value = "fetch: " + item.shortdesc

    def pulse(self, owner): # pylint: disable=unused-argument
        self._float_progress.value = self.current_items / self.total_items
        return True

    def status_change(self, pkg, percent, status):
        self._label.value = "%s: %s" % (pkg, status)
        self._float_progress.value = percent / 100.0

    def update(self, percent=None): # pylint: disable=unused-argument
        self._float_progress.value = self.percent / 100.0
        self._label.value = self.op + ": " + self.subop

    def done(self, item=None):
        pass
