from .Basecontroller import Basecontroller
from.projectconroller import Projectcontroller
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from models import processingenum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class processcontroller(Basecontroller):
    def __init__(self, project_id: str):
       super().__init__()
       self.project_id = project_id
       self.project_path = Projectcontroller().get_project_path(project_id = project_id)



    def get_extension_file(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    

    def get_file_loader(self, file_id : str, file_path: str):
        file_ext = self.get_extension_file(file_id = file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if file_ext == processingenum.TXT.value:
            return TextLoader(file_path, encoding = "utf-8")
        
        if file_ext == processingenum.PDF.value:
            return PyPDFLoader(file_path)
        
        return None
    

    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id = file_id)
        return loader.load()

    def process_file_content(self, file_content: list, file_id: str, chunh_size: int = 100, overlap_size: int = 20):

        text_splitter = RecursiveCharacterTextSplitter(chunh_size = chunh_size, chunk_overlap = overlap_size, length_function = len)

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunk = text_splitter.create_documents(
            file_content_texts,
            metadatas = file_content_metadata
        )

        return chunk