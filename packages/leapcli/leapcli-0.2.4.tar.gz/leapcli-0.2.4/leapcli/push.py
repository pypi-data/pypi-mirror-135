import importlib.util
import tempfile
import hashlib
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

import requests
from openapi_client.model.dataset_parse_request_params import DatasetParseRequestParams
from openapi_client.model.external_import_model_storage import ExternalImportModelStorage
from openapi_client.model.save_dataset_version_params import SaveDatasetVersionParams
from openapi_client.models import GetUploadSignedUrlParams, ImportNewModelParams, ImportModelType, \
    ExternalImportModelStorageResponse, GetCurrentProjectVersionParams

from leapcli.project import Project
from leapcli.login import Authenticator
from leapcli.exceptions import ModelNotFound, ModelEntryPointNotFound, ModelSaveFailure, \
    ModelNotSaved

_log = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class Push:
    def __init__(self, project: Project):
        self.project = project

        Authenticator.initialize(self.project)
        self._api = Authenticator.authenticated_api()

    @staticmethod
    def file_sha(path: Path) -> str:
        file_hash = hashlib.sha256()
        block_size = 2 ** 16
        with open(path, 'rb') as f:
            chunk = f.read(block_size)
            while len(chunk) > 0:
                file_hash.update(chunk)
                chunk = f.read(block_size)  # Read the next block from the file
            return file_hash.hexdigest()

    def get_import_url(self, filename: str) -> Tuple[str, str]:
        params = GetUploadSignedUrlParams(filename)
        import_url_response: ExternalImportModelStorage = self._api.get_upload_signed_url(params)
        return import_url_response.url, import_url_response.file_name

    @staticmethod
    def upload_file(url: str, path: Path) -> None:
        with open(path, 'rb') as f:
            requests.put(url, f, headers={"content-type": "application/octet-stream"})

    def current_project_version(self) -> str:
        proj_id = self.project.project_id(self._api)
        return self._api.get_current_project_version(GetCurrentProjectVersionParams(proj_id)).version_id

    def start_import_job(self, filename: str) -> str:
        proj_id = self.project.project_id(self._api)
        version = self.current_project_version()
        generated_model_name = f'CLI_{datetime.utcnow().strftime("%m/%d/%Y_%H:%M:%S")}'
        params = ImportNewModelParams(proj_id, filename, generated_model_name, version, ImportModelType('H5_TF2'))
        response: ExternalImportModelStorageResponse = self._api.import_model(params)
        return response.import_model_job_id

    def import_model(self, content_hash: str, path: Path) -> str:
        url, file_name = self.get_import_url(content_hash)
        Push.upload_file(url, path)
        return self.start_import_job(file_name)

    def _parse_dataset(self, dataset_py_as_string: str):
        dataset_id = self.project.dataset_id(self._api)
        params = DatasetParseRequestParams(dataset_id, is_public_bucket=False, script=dataset_py_as_string)
        self._api.parse_dataset(params)

    def _save_dataset(self, dataset_py_as_string: str):
        dataset_id = self.project.dataset_id(self._api)

        params = SaveDatasetVersionParams(dataset_id, bucket=self.project.detect_bucket(), script=dataset_py_as_string,
                                          save_as_new=False, is_public_bucket=False, is_valid=False)
        self._api.save_dataset_version(params)

    def save_and_parse_dataset(self):
        dataset_py_path = self.project.dataset_py_path()
        with open(str(dataset_py_path), "r") as f:
            dataset_py_as_string = f.read()
        self._save_dataset(dataset_py_as_string)

    @staticmethod
    def load_model_config_module(model_py_path: Path):
        if not model_py_path.is_file():
            raise ModelNotFound()

        spec = importlib.util.spec_from_file_location('tensorleap.model', model_py_path)
        model_module = importlib.util.module_from_spec(spec)

        sys.modules['tensorleap.model'] = model_module
        spec.loader.exec_module(model_module)
        return model_module

    # TODO: un-hardcode the .h5 suffix
    # Returns path to serialized model in cache dir and content content_hash of the file
    def serialize_model(self) -> Tuple[Path, str]:
        model_py_path = self.project.model_py_path()
        _log.debug('Looking for model integration file', extra=dict(path=model_py_path))

        if not model_py_path.is_file():
            raise ModelNotFound()

        _log.info('Loading user model configuration', extra=dict(path=model_py_path))
        model_module = Push.load_model_config_module(model_py_path)

        if not hasattr(model_module, 'leap_save_model'):
            raise ModelEntryPointNotFound()

        _, tmp_h5 = tempfile.mkstemp(suffix='.h5')
        tmp_h5 = Path(tmp_h5)

        _log.info('Invoking user leap_save_model', extra=dict(tgt_path=tmp_h5))
        try:
            model_module.leap_save_model(tmp_h5)
        except Exception as error:
            raise ModelSaveFailure() from error

        # Don't accumulate temp files with identical content
        # TODO: future enhancement: don't uploads to server if already uploaded before

        # File could exist but have 0 bytes because of mktemp
        if not tmp_h5.exists() or tmp_h5.stat().st_size == 0:
            raise ModelNotSaved()
        content_hash = Push.file_sha(tmp_h5)
        cache_path = self.project.cache_dir().joinpath(content_hash + '.h5')
        tmp_h5.rename(cache_path)

        return cache_path, content_hash

    def run(self):
        path, content_hash = self.serialize_model()
        self.import_model(content_hash, path)
        self.save_and_parse_dataset()

        print('Push command successfully complete')
