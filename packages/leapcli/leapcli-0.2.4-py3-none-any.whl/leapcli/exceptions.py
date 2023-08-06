import sys


class AlreadyInitialized(Exception):
    pass


class InvalidProjectName(Exception):
    pass


class ProjectNotInitialized(Exception):
    pass


class CredentialsNotFound(Exception):
    pass


class InvalidOrgName(Exception):
    pass


class MalformedKeys(Exception):
    pass


class KeysMixedUp(Exception):
    pass


class LoginFailed(Exception):
    pass


class ModelNotFound(Exception):
    pass


class ParseDatasetFailed(Exception):
    pass


class ModelEntryPointNotFound(Exception):
    pass


class ModelSaveFailure(Exception):
    def __init__(self):
        super().__init__()
        self.exc_type, self.inner_exception, self.traceback = sys.exc_info()


class DoctorCheckFailed(Exception):
    def __init__(self):
        super().__init__()
        self.exc_type, self.inner_exception, self.traceback = sys.exc_info()


class ModelNotSaved(Exception):
    pass
