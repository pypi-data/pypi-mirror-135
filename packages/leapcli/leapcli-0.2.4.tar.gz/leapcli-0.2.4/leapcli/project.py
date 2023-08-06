import enum
import os
import logging
import tempfile
from pathlib import Path
import re
from shutil import copytree
from typing import Optional

from toml import load, dump
from git import Repo
from git.exc import InvalidGitRepositoryError
import toml
from openapi_client.apis import DefaultApi

from leapcli.exceptions import InvalidOrgName, CredentialsNotFound, AlreadyInitialized, InvalidProjectName


class Framework(str, enum.Enum):
    TENSORFLOW = 'tensorflow'
    PYTORCH = 'pytorch'


TENSORLEAP_DIR = '.tensorleap'
CONFIG_DIR = '~/.config/tensorleap'

VALID_PROJECT_REGEX = r'^[a-zA-Z0-9_\-.]{3,}$'
VALID_PROJECT_EXPL = '''* At least 3 characters long.
* Allowed characters: alphanumeric, "_", "-", "."'''

VALID_ORG_REGEX = r'^[a-zA-Z0-9][a-zA-Z0-9\-]+[a-zA-Z0-9]$'
VALID_ORG_EXPL = '''* At least 3 characters long.
* Allowed characters: alphanumeric, "-"
* Does not start or end with a hyphen.
* No double hypens.'''

CONFIG_FILENAME = 'config.toml'

TENSORLEAP_BACKEND_DOMAIN = 'tensorleap.ai'

_log = logging.getLogger(__name__)


class Project:
    def __init__(self, directory: str = '.'):
        self.directory: Path = Path(directory)
        self.project: Optional[str] = None
        self.org: Optional[str] = None
        self.framework: Framework = Framework.TENSORFLOW
        self.state = {}
        self.dataset: Optional[str] = None
        self.bucket: Optional[str] = None

    def detect_project_dir(self) -> Path:
        try:
            repo = Repo(self.directory, search_parent_directories=True)
            return repo.working_tree_dir
        except InvalidGitRepositoryError:
            return os.getcwd()

    def detect_project(self) -> str:
        if self.is_initialized():
            return self.project_config()['projectName']
        raise CredentialsNotFound()

    def detect_dataset(self) -> str:
        if self.is_initialized():
            return self.project_config()['datasetName']
        raise CredentialsNotFound()

    def detect_bucket(self) -> str:
        if self.is_initialized():
            return self.project_config()['bucketName']
        raise CredentialsNotFound()

    @staticmethod
    def prompt_dataset() -> str:
        return input('Dataset name: ')

    @staticmethod
    def prompt_project() -> str:
        return input('Project name: ')

    def org_domain(self) -> str:
        return f'{self.detect_org()}.{TENSORLEAP_BACKEND_DOMAIN}'

    def detect_backend_url(self) -> str:
        assert self.is_initialized()
        if 'apiEndpoint' in self.project_config():
            _log.debug('found apiEndpoint override in config')
            return self.project_config()['apiEndpoint']
        return f'{self.home_url()}/api/v2'

    def project_id(self, api: DefaultApi) -> str:
        # TODO: cache this result
        matches = [proj.id for proj in api.get_projects().data if proj.name == self.detect_project()]
        assert len(matches) == 1
        return matches[0]

    def dataset_id(self, api: DefaultApi) -> str:
        # TODO: cache this result
        matches = [dataset.id for dataset in api.get_datasets().datasets if dataset.name == self.detect_dataset()]
        assert len(matches) == 1
        return matches[0]

    def home_url(self) -> str:
        return f'https://{self.org_domain()}'

    def cache_dir(self) -> Path:
        self.read_state()
        if 'cache_dir' in self.state:
            return Path(self.state['cache_dir'])
        cache_dir = tempfile.mkdtemp(prefix='tensorleap-cache')
        self.state['cache_dir'] = cache_dir
        self.save_state()
        return Path(cache_dir)

    @staticmethod
    def leapcli_state_file() -> Path:
        return Project.config_dir().joinpath('state.toml')

    def read_state(self) -> dict:
        if Project.leapcli_state_file().is_file():
            with open(Project.leapcli_state_file(), encoding='utf-8') as f:
                self.state = load(f)
        return self.state

    def save_state(self) -> None:
        with open(Project.leapcli_state_file(), 'w', encoding='utf-8') as f:
            dump(self.state, f)

    @staticmethod
    def leapcli_package_dir() -> Path:
        return Path(__file__).parent.parent

    @staticmethod
    def leapcli_package_info() -> dict:
        poetry_conf_file = Project.leapcli_package_dir(). \
            joinpath('pyproject.toml')
        with open(poetry_conf_file, encoding='utf-8') as f:
            return toml.load(f)

    @staticmethod
    def template_dir() -> Path:
        return Project.leapcli_package_dir().joinpath('templates')

    @staticmethod
    def org_from_remote_url(url: str) -> str:
        if url is None:
            return None

        # Expect pattern: git@some.domain:tensorleap/cli.git
        git_url_pattern = r'git@(?:\w+\.)+\w+:([^/]+)/.*'
        git_url_match = re.match(git_url_pattern, url)
        if git_url_match is not None:
            return git_url_match[1]

        # Expect https://gitlab.com/gitlab-org/gitlab-foss.git
        https_url_pattern = r'https://(?:\w+\.)+\w+/([^/]+)/.*'
        https_url_match = re.match(https_url_pattern, url)
        if https_url_match:
            return https_url_match[1]
        return None

    def detect_org(self) -> str:
        if self.is_initialized():
            return self.project_config()['organization']
        try:
            repo = Repo(self.directory)
            origin_remote = next((r for r in repo.remotes if r.name == 'origin'), None)
            if origin_remote is None:
                return None
            return Project.org_from_remote_url(origin_remote.url)
        except InvalidGitRepositoryError:
            return None

    @staticmethod
    def config_dir() -> Path:
        ret = Path(CONFIG_DIR).expanduser()
        ret.mkdir(parents=True, exist_ok=True)
        return ret

    def prompt_org(self) -> str:
        default = self.detect_org()
        if default is None:
            choice = input('Organization: ')
            if not choice:
                raise InvalidOrgName()
            return choice
        return input(f'Organization ({default}): ') or default

    def tensorleap_dir(self) -> Path:
        return self.directory.joinpath(TENSORLEAP_DIR)

    @staticmethod
    def validate_project_name(name: str) -> None:
        if not name or re.match(VALID_PROJECT_REGEX, name) is None:
            raise InvalidProjectName()

    @staticmethod
    def validate_org_name(name: str) -> None:
        if not name or re.match(VALID_ORG_REGEX, name) is None \
                or '--' in name or len(name) < 3:
            raise InvalidOrgName()

    def is_initialized(self):
        return self.tensorleap_dir().is_dir()

    def init_project(self, framework: Framework, project: str, org: str, dataset: str, bucket: str):
        if self.is_initialized():
            raise AlreadyInitialized()
        self.project = project or self.prompt_project()
        Project.validate_project_name(self.project)
        self.org = org
        Project.validate_org_name(self.org)
        self.dataset = dataset
        self.framework = framework
        self.bucket = bucket
        self._generate_project_template()

    def config_file_path(self) -> Path:
        return self.tensorleap_dir().joinpath(CONFIG_FILENAME)

    def project_config(self) -> dict:
        with open(self.config_file_path(), 'r', encoding='utf-8') as config_file:
            _log.debug('reading stored config from %s', self.config_file_path())
            return toml.load(config_file)

    def _generate_project_template(self):
        assert self.project
        assert self.org
        assert not self.tensorleap_dir().is_dir()

        tgt = self.tensorleap_dir()
        copytree(Project.template_dir().joinpath(TENSORLEAP_DIR), tgt)
        txt = ''
        with open(self.config_file_path(), 'r', encoding='utf-8') as config_file:
            txt = config_file.read()
            txt = txt.replace('PROJ', self.project)
            txt = txt.replace('ORG', self.org)
            txt = txt.replace('FRAMEWORK', self.framework)
            txt = txt.replace('DATASET', self.dataset)
            txt = txt.replace('BUCKET', self.bucket)

        with open(self.config_file_path(), 'w', encoding='utf-8') as config_file:
            config_file.write(txt)

    def _integration_file_py_path(self, file_name: str) -> Path:
        file_py = self.project_config()['integration'][file_name]
        return self.tensorleap_dir().joinpath(file_py)

    def model_py_path(self) -> Path:
        return self._integration_file_py_path('model')

    def dataset_py_path(self) -> Path:
        return self._integration_file_py_path('dataset')
