import os
import uuid


class LocalStore():
    def __init__(self, project):
        ensure_dir(os.path.join(os.path.expanduser('~'), '.trackdog'))
        self.logger = logging.getLogger(__name__)
        self._project = get_project(project)

    @property
    def project(self):
        return self.project

    @classmethod()
    def get_project(project):
        if project is None:
            return str(uuid.uuid4())
        return project
