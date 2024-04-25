import json
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

    def get_file_infos(self, directory_path, upload_date: datetime) -> list[FileInfo]:
        file_infos = []
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
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

    def list_files(self, project_id: str) -> list[FileInfo]:
        project_directories = [d for d in os.listdir(self.upload_dir) if d.startswith(f'project_{project_id}_')]
        if not project_directories:
            return []

        latest_directory = sorted(project_directories, key=lambda x: (x.split('_')[2], x.split('_')[3]), reverse=True)[
            0]
        latest_directory_path = os.path.join(self.upload_dir, latest_directory)
        upload_date = datetime.fromtimestamp(os.path.getctime(latest_directory_path))

        return self.get_file_infos(latest_directory_path, upload_date)

    def get_latest_upload_path(self, project_id: str) -> str | None:
        project_directories = [d for d in os.listdir(self.upload_dir) if d.startswith(f'project_{project_id}_')]
        if not project_directories:
            return None

        latest_directory = sorted(project_directories, key=lambda x: (x.split('_')[2], x.split('_')[3]), reverse=True)[
            0]
        return os.path.join(self.upload_dir, latest_directory)

    def parse_files(self, src_directory_path: str):
        parsed_files = []

        upload_date = datetime.fromtimestamp(os.path.getctime(src_directory_path))
        files = self.get_file_infos(src_directory_path, upload_date)

        for file in files:
            parser = ParserFactory.get_parser(file.path)
            parsed_file = parser.parse(file.path)
            parsed_files.extend(parsed_file)

        return parsed_files

    def dump_list_to_json(self, parsed_files: list[str], dest_directory_path: str, dest_file_name: str):
        if not os.path.isabs(dest_directory_path):
            raise ValueError("Destination path must be absolute")

        if not dest_file_name.endswith('.json'):
            dest_file_name += '.json'

        file_path = os.path.join(dest_directory_path, dest_file_name + '.json')
        os.makedirs(dest_directory_path, exist_ok=True)

        if os.path.exists(file_path):
            raise FileExistsError(f"The file {file_path} already exists.")

        try:
            stringify_parsed_files = [str(elem) for elem in parsed_files]
            with open(file_path, 'w') as f:
                json.dump(stringify_parsed_files, f, indent=4)
        except (IOError, OSError) as e:
            raise Exception(f"Failed to write to {file_path}: {str(e)}")
        except TypeError as e:
            raise Exception(f"Data serialization error: {str(e)}")
