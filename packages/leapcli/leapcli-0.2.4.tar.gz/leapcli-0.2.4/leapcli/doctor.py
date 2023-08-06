import logging
import sys
import traceback
from functools import lru_cache
from typing import Optional

import luddite
import pkg_resources
from code_loader import DatasetLoader
from openapi_client.api.default_api import DefaultApi
from openapi_client.exceptions import NotFoundException, UnauthorizedException
from semver import VersionInfo

from leapcli.project import Project
from leapcli.login import Authenticator
from leapcli.exceptions import LoginFailed, DoctorCheckFailed
import leapcli.exceptions
from leapcli.push import Push

_log = logging.getLogger(__name__)

BANNER = '''
****************************************************
*                  Tensorleap CLI                  *
*                  --------------                  *
*                   health check                   *
****************************************************
'''

SCREEN_WIDTH = len(BANNER.split('\n')[1])


def format_kv(key: str, val: str) -> str:
    padding = SCREEN_WIDTH - len(key) - len(val) - 1
    assert padding > 0
    return f'{key}:{" " * padding}{val}'


# Prints key aligned to left and value to right.
def print_kv(key: str, val: str):
    print(format_kv(key, val))


def yesnobool(value: bool) -> str:
    return 'yes' if value else 'no'


class Doctor:
    def __init__(self, project: Project):
        self.project = project
        self._api: Optional[DefaultApi] = None

    def _get_api(self) -> DefaultApi:
        if self._api is None:
            self._api = Authenticator.authenticated_api()
        return self._api

    @staticmethod
    @lru_cache(1)
    def latest_cli_version() -> VersionInfo:
        return VersionInfo.parse(luddite.get_version_pypi("leapcli"))

    @staticmethod
    @lru_cache(1)
    def current_cli_version() -> VersionInfo:
        return VersionInfo.parse(pkg_resources.get_distribution("leapcli").version)

    @lru_cache(1)
    def update_available(self):
        return VersionInfo.compare(self.current_cli_version(),
                                   self.latest_cli_version()) < 0

    def check_cli(self):
        print_kv('Tensorleap CLI version', str(self.current_cli_version()))
        update = 'no'
        if self.update_available():
            update = f'yes ({str(self.latest_cli_version())})'
        print_kv('CLI update available', update)

    def check_project(self):
        print('\n* Inspecting project settings...\n')
        initialized = self.project.is_initialized()
        init = yesnobool(initialized)
        print_kv('Project initialized', init)
        if not initialized:
            print("\nRun `leap init` in your project's root directory.")
            raise DoctorCheckFailed()
        print_kv('Organization', self.project.detect_org())
        print_kv('Home URL', self.project.home_url())
        print_kv('Project name', self.project.detect_project())
        print_kv('Framework', self.project.framework)
        print_kv('Dataset name', self.project.detect_dataset())
        print_kv('Bucket name', self.project.detect_bucket())

    def check_model(self) -> bool:
        path, _ = Push(self.project).serialize_model()
        return path.is_file()

    def check_dataset(self):
        dataset_py_path = self.project.dataset_py_path()
        with open(str(dataset_py_path), "r") as f:
            dataset_py_as_string = f.read()
        dataset_loader = DatasetLoader(dataset_py_as_string)
        dataset_parse_result = dataset_loader.check_dataset()
        if not dataset_parse_result.is_valid:
            print('\nFailed to parse dataset script.\n')
            error_message = dataset_parse_result.general_error
            if error_message is None:
                error_message = str([payload.display for payload in dataset_parse_result.payloads
                                     if not payload.is_passed])
            print(error_message)
            raise leapcli.exceptions.ParseDatasetFailed()
        print_kv('Dataset parse', 'ok')

    def check_codebase(self):
        print('\n* Inspecting model...\n')
        try:
            if self.check_model():
                print_kv('Model serialization', 'ok')
            self.check_dataset()
            return
        except leapcli.exceptions.ModelNotFound:
            print_kv('Model serialization', 'error')
            expected_model_path = self.project.model_py_path()
            print(f'\nFailed to load model configuration.\n'
                  f'Path: {expected_model_path}')
        except leapcli.exceptions.ModelEntryPointNotFound:
            print_kv('Model serialization', 'error')
            expected_model_path = self.project.model_py_path()
            print(f'\nleap_save_model(path) function not found in model\n'
                  f'configuration file.\n'
                  f'\n'
                  f'Path: {expected_model_path}')
        except leapcli.exceptions.ModelNotSaved:
            print_kv('Model serialization', 'error')
            expected_model_path = self.project.model_py_path()
            print('\nleap_save_model(path) ran by did not save the model\n'
                  'to the given .h5 file.')
        except leapcli.exceptions.ModelSaveFailure as error:
            print_kv('Model serialization', 'error')
            print('\nleap_save_model(path) raised an exception.\n')
            print(type(error.inner_exception))
            traceback.print_exception(error.exc_type,
                                      error.inner_exception,
                                      error.traceback,
                                      file=sys.stdout)

        except Exception:  # pylint: disable=broad-except
            print_kv('Model serialization', 'error')
            print('Unknown error trying to save the model')
            traceback.print_exc()

        raise DoctorCheckFailed()

    def check_creds(self):
        print('\n* Inspecting credentials...')
        if not Authenticator.has_credentials():
            domain = self.project.org_domain()
            # TODO: use the real URL once this screen is implemented
            # in the web UI
            url = f'https://{domain}/profile/api-keys'
            print(f'\n'
                  f'Credentials not found.\n'
                  f'\n'
                  f'You can generate an API key at:\n'
                  f'  {url}\n')
            raise DoctorCheckFailed()
        try:
            Authenticator.initialize(self.project)

            print()
            print_kv('Logged in as', Authenticator.user.local.email)
            return True
        except (UnauthorizedException, NotFoundException, LoginFailed):
            print('\n'
                  'Login failed with the configured credentials.\n'
                  '\n'
                  'Try running `leap login` again.\n')
            raise DoctorCheckFailed()

    def check_project_exist(self):
        try:
            print('\n* Finding project...\n')
            project_id = self.project.project_id(self._get_api())
            print_kv("Project found. ID", project_id)
            return
        except AssertionError:
            print(f'Did not find project named {self.project.project}. Please create new project using the web UI or \n'
                  f'            run leap init and change to exist project.')
        raise DoctorCheckFailed()

    def check_dataset_exist(self):
        try:
            print('\n* Finding dataset...\n')
            dataset_id = self.project.dataset_id(self._get_api())
            print_kv("Dataset found. ID", dataset_id)
            return
        except AssertionError:
            print(f'Did not find dataset named {self.project.dataset}. Please create new dataset using the web UI or \n'
                  f'            run leap init and change to exist dataset.')
        raise DoctorCheckFailed()

    def run(self):
        print(BANNER)
        try:
            self.check_cli()
            self.check_project()
            self.check_creds()
            self.check_project_exist()
            self.check_dataset_exist()
            self.check_codebase()
        except DoctorCheckFailed:
            print('Check failed.')
