import json
from typing import Dict

from .abstract import ParameterStorageAbstract
from .infrastructure.s3 import S3Client


class S3ParameterStorage(ParameterStorageAbstract):
    def __init__(self, s3: S3Client):
        self._s3 = s3

    @staticmethod
    def _filename(task_type: str, task_id: str) -> str:
        return f'{task_type}/{task_id}.json'

    def upload(self, task_type: str, task_id: str, params: Dict):
        data = json.dumps(params, ensure_ascii=False)
        filename = self._filename(task_type, task_id)
        self._s3.upload(data, filename)

    def fetch_parameters(self, task_type: str, task_id: str) -> Dict:
        filename = self._filename(task_type, task_id)
        data = self._s3.read(filename)
        return json.loads(data)
