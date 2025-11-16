from enum import Enum

class Responsesignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_NOT_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    processing_SUCCESS = "processing_success"
    processing_Failed = "processing_failed"
    
