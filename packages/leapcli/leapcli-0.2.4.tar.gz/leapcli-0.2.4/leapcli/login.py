import re
import logging
from pathlib import Path
from typing import Optional, Tuple

from toml import load, dump
from openapi_client import Configuration, ApiClient
from openapi_client.models import KeyLoginParams, UserData
from openapi_client.apis import DefaultApi
from leapcli.exceptions import MalformedKeys, KeysMixedUp, LoginFailed, CredentialsNotFound
from leapcli.project import Project

CREDENTIALS_FILENAME = 'credentials.toml'

_log = logging.getLogger(__name__)


class _Authenticator:
    def __init__(self):
        self._api_id: Optional[str] = None
        self._api_key: Optional[str] = None
        self._api_client: Optional[DefaultApi] = None
        self._project: Optional[Project] = None
        self.user: Optional[UserData] = None
        self.cookie: Optional[str] = None
        self.is_initialized = False

    def initialize(self, project: Project, api_id: Optional[str] = None,
                   api_key: Optional[str] = None, should_write_credentials=False):
        self._project = project
        self._api_key = api_key
        self._api_id = api_id
        if not api_key or not api_id:
            self._api_id, self._api_key = _Authenticator.read_credentials()

        if not self._api_key or not self._api_id:
            raise CredentialsNotFound()

        if not _Authenticator.is_valid_api_id(self._api_id):
            if _Authenticator.is_valid_api_key(self._api_id):
                raise KeysMixedUp()
            raise MalformedKeys()

        if not _Authenticator.is_valid_api_key(self._api_key):
            raise MalformedKeys()

        self.authenticated_api()

        if should_write_credentials:
            self.write_credentials(self._api_id, self._api_key)

        self.is_initialized = True

    @staticmethod
    def redact_key(key: str) -> str:
        assert len(key) > 3
        # Mask the first 19 characters of a key
        return '*' * 19 + key[-3:]

    @staticmethod
    def is_valid_api_key(api_key: str) -> bool:
        return re.match(r'^k0\w{20}$', api_key) is not None

    @staticmethod
    def is_valid_api_id(api_id: str) -> bool:
        return re.match(r'^i0\w{20}$', api_id) is not None

    @staticmethod
    def credentials_file_path() -> Path:
        return Project.config_dir().joinpath(CREDENTIALS_FILENAME)

    @staticmethod
    def has_credentials() -> bool:
        api_id, api_key = _Authenticator.read_credentials()
        return api_id is not None and api_key is not None

    @staticmethod
    def read_credentials() -> Tuple[Optional[str], Optional[str]]:
        # TODO: more robust handling of corrupted file
        path = _Authenticator.credentials_file_path()
        if path.is_file():
            _log.debug('reading credentials from %s', path)
            with path.open('r') as f:
                dictionary = load(f)
                return dictionary['api_id'], dictionary['api_key']
        return None, None

    @staticmethod
    def write_credentials(api_id: str, api_key: str) -> None:
        _log.info('writing credentials')
        with _Authenticator.credentials_file_path().open('w') as f:
            return dump(dict(api_id=api_id, api_key=api_key), f)

    def key_login(self) -> None:
        host = self._project.detect_backend_url()
        cfg = Configuration(host=host)
        unauthenticated_client = ApiClient(cfg)
        api = DefaultApi(unauthenticated_client)
        params = KeyLoginParams(self._api_id, self._api_key)
        user, status, headers = api.key_login(params, _return_http_data_only=False)
        if status != 200 or not 'Set-Cookie' in headers:
            _log.info('login failed with api_id: %s, api_key: %s', self._api_id,
                      self.redact_key(self._api_key))
            raise LoginFailed()
        self.user = user
        self.cookie = headers['Set-Cookie']

    # @staticmethod
    # def load_credentials() -> None:
    #     Authenticator.api_id = Authenticator.detect_api_id()
    #     Authenticator.api_key = Authenticator.detect_api_key()

    def logged_in(self) -> bool:
        return self.cookie is not None

    def authenticated_api(self) -> DefaultApi:
        if not self.logged_in():
            self.key_login()
        host = self._project.detect_backend_url()
        cfg = Configuration(host=host)
        cookie_client = ApiClient(cfg, cookie=self.cookie)

        return DefaultApi(cookie_client)


Authenticator = _Authenticator()
