from config import settings
from files.service import FileUploadService


def get_file_upload_service() -> FileUploadService:
    return FileUploadService(upload_dir=settings.FILE_UPLOAD_PATH)
