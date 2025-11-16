from .Basecontroller import Basecontroller
from fastapi import UploadFile
from .projectconroller import Projectcontroller
from models import Responsesignal
import re
import os

class Datacontroller(Basecontroller):
    def __init__(self):
        super().__init__()
        self.scale = 1048576


    def validation_upload_file(self, file: UploadFile):

        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False, Responsesignal.FILE_TYPE_NOT_SUPPORTED.value
            
        if file.size > self.app_settings.FILE_MAX_SIZE * self.scale:
            return False, Responsesignal.FILE_SIZE_NOT_EXCEEDED.value
        
        return True, Responsesignal.FILE_UPLOAD_SUCCESS.value
    


    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        
        random_filename = self.generate_random_string()
        project_path = Projectcontroller().get_project_path(project_id = project_id)

        cleaned_file_name = self.get_clean_file_name(orig_file_name = orig_file_name)

        new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_file_name)

        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_file_name)

        return new_file_path, random_filename + "_" + cleaned_file_name   



    def get_clean_file_name(self, orig_file_name):
        
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name    
