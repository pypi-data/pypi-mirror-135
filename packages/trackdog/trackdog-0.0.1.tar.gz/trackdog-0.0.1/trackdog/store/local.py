import logging
import os
import uuid

from trackdog.store.util import ensure_dir, ensure_file


class LocalStore():
    def __init__(self, project=None, run=None):
        self.logger = logging.getLogger(__name__)
        self._project = LocalStore.get_project(project)
        self._run = LocalStore.get_run(run)
        self._run_path = os.path.join(os.path.expanduser("~"),
                                      ".trackdog/{}/{}".format(self._project, self._run))
        ensure_dir(self._run_path)

    @property
    def project(self):
        return self._project

    @property
    def run(self):
        return self._run

    @classmethod
    def get_project(cls, project):
        if project is None:
            return str(uuid.uuid4())
        return project

    @classmethod
    def get_run(cls, run):
        if run is None:
            return str(uuid.uuid4())
        return run

    def track(self, val, name, epoch=None, step=None):
        self.logger.debug('storing metric %s for project %s, run %s',
                          name, self.project, self.run)
        f_name = os.path.join(self._run_path, "{}.txt".format(name))
        ensure_file(f_name)
        with open(f_name, "w") as f:
            f.write("{} {} {}\n".format(val, epoch, step))
