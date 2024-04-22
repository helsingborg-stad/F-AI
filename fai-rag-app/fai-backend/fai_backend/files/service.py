import mimetypes
import os
import uuid
from datetime import datetime

from fastapi import UploadFile
from pydantic import ByteSize

from fai_backend.files.file_parser import ParserFactory
from fai_backend.files.models import FileInfo


class FileUploadService:
    def __init__(self, upload_dir: str):
        self.upload_dir = os.path.abspath(upload_dir)
        os.makedirs(self.upload_dir, exist_ok=True)

    def _generate_upload_path(self, project_id: str) -> str:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        upload_session_uuid = str(uuid.uuid4())
        path = f'project_{project_id}_{timestamp}_{upload_session_uuid}'
        full_path = os.path.join(self.upload_dir, path)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def save_files(self, project_id: str, files: list[UploadFile]) -> str:
        upload_path = self._generate_upload_path(project_id)

        for file in files:
            file_location = os.path.join(upload_path, file.filename)
            with open(file_location, 'wb+') as file_object:
                file_object.write(file.file.read())
        return upload_path

    def list_files(self, project_id: str) -> list[FileInfo]:
        project_directories = [d for d in os.listdir(self.upload_dir) if d.startswith(f'project_{project_id}_')]
        if not project_directories:
            return []

        latest_directory = sorted(project_directories, key=lambda x: (x.split('_')[2], x.split('_')[3]), reverse=True)[
            0]
        latest_directory_path = os.path.join(self.upload_dir, latest_directory)
        upload_date = datetime.fromtimestamp(os.path.getctime(latest_directory_path))

        file_infos = []
        for file_name in os.listdir(latest_directory_path):
            file_path = os.path.join(latest_directory_path, file_name)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                file_infos.append(FileInfo(
                    file_name=file_name,
                    file_size=ByteSize(stat.st_size),
                    path=file_path,
                    mime_type=mime_type or 'application/octet-stream',
                    last_modified=datetime.fromtimestamp(stat.st_mtime),
                    upload_date=upload_date,
                    created_date=datetime.fromtimestamp(stat.st_ctime)
                ))

        return file_infos

    def get_latest_upload_path(self, project_id: str) -> str | None:
        project_directories = [d for d in os.listdir(self.upload_dir) if d.startswith(f'project_{project_id}_')]
        if not project_directories:
            return None

        latest_directory = sorted(project_directories, key=lambda x: (x.split('_')[2], x.split('_')[3]), reverse=True)[
            0]
        return os.path.join(self.upload_dir, latest_directory)

    def parse_uploaded_files(self, project_id: str) -> list:
        parsed_files = []

        latest_upload_path = self.get_latest_upload_path(project_id)
        if not latest_upload_path:
            return parsed_files

        uploaded_files = self.list_files(project_id)

        for file in uploaded_files:
            parser = ParserFactory.get_parser(file.path)
            parsed_files.append(parser.parse(file.path))

        return parsed_files
