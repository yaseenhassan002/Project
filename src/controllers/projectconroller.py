from .Basecontroller import Basecontroller
from fastapi import UploadFile
from models import Responsesignal
import os

class Projectcontroller(Basecontroller):
    def __init__(self):
        super().__init__()


    def get_project_path(self, project_id: str):
        project_dir = os.path.join(
            self.base_dir,
            project_id
        )

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir    