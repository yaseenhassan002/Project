from fastapi import FastAPI, File, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import Datacontroller, Projectcontroller, processcontroller
import os
import aiofiles
from models import Responsesignal
import logging
from .schemes.data import processRequest
from models.ProjectDataModel import ProjectDataModel 
from models import ChunkDatamodel 
from models.dB_shemes import Datachunk
from models.ChunkDatamodel import cchunkDatamodel


logger = logging.getLogger("unicorn.error")

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")


async def upload_data(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    data_controller = Datacontroller()
    is_valid, result_signal = data_controller.validation_upload_file(file = file)
    await file.seek(0)

    
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
            "signal": result_signal
            }
        )
    

    project_dir_path = Projectcontroller().get_project_path(project_id = project_id)
    file_path, file_id = data_controller.generate_unique_file(
        orig_file_name = file.filename,
        project_id = project_id 
        )

    try:
        async with aiofiles.open(file_path, "wb") as f:
          while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    
    except Exception as e:
       
       logger.error(f"Error while uploading file: {e}")
       return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
            "signal": Responsesignal.FILE_UPLOAD_FAILED.value
            }
        )
                

    return JSONResponse(
        content = {
            "signal": Responsesignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id
        }
    )


@data_router.post("/process/{project_id}")

async def process_endpoint(request: Request, project_id: str, process_Request: processRequest):
   
   file_id = process_Request.file_id
   chunk_size = process_Request.chunk_size
   overlap_size = process_Request.overlap_size
   do_reset = process_Request.do_reset

   project_model = await ProjectDataModel.create_instance(
      db_client = request.app.db_client
   )

   project = await project_model.get_project_or_create_one(project_id = project_id)

   process_controller = processcontroller(project_id = project_id)

   file_content = process_controller.get_file_content(file_id = file_id)

   file_chunk = process_controller.process_file_content(
      file_content = file_content,
      file_id = file_id,
      chunh_size = chunk_size,
      overlap_size = overlap_size)
   
   if file_chunk is None or len(file_chunk)== 0:
      return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = {
           "signal": Responsesignal.processing_Failed.value,
        
           
        }
      )

   file_chunk_records = [
      Datachunk(chunk_text = chunk.page_content,
                chunk_metadata= chunk.metadata,
                chunk_order = i+1,
                chunk_project_id = project.id)
        for i, chunk in enumerate(file_chunk)]
   
   chunk_model = await cchunkDatamodel.create_instances(
      db_client = Request.app.db_client)
   
   if do_reset==1:
     await chunk_model.delete_chunks_by_project_id_(
         project_id = project.id
      )
   

   no_record = await cchunkDatamodel.insert_many_chunk(Chunks = file_chunk_records)

   return JSONResponse(
      content={
        "signal":Responsesignal.processing_SUCCESS.value,
        "inserted_chunks": no_record
      }
   )
