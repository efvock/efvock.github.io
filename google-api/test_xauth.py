import pytest
from pathlib import Path
from xauth import (
    cred_cache,
    cred_cache_path,
    google_service,
    google_service_ex,
    xauth,
    SECRETS_DIR,
)

SCOPES_MAIL, SCOPES_DRIVE = (
    ["https://www.googleapis.com/auth/gmail.readonly"],
    ["https://www.googleapis.com/auth/drive.file"],
)

CRED_MAIL = cred_cache_path(SCOPES_MAIL, "gmail", "v1")
CRED_DRIVE = cred_cache_path(SCOPES_DRIVE, "drive", "v3")


def test0cred_cache():
    scopes = ["https://x.com/ab/c.d", "file:///pq/r.s"]
    cache = cred_cache(scopes, "service", "version")
    assert cache == "google-api_service_version_ab-c.d--pq-r.s"


def test1xauth0(_clean, creds):
    _clean
    assert creds


def test1xauth1(creds):
    assert creds


def test2google_service0mail(creds):
    assert google_service("gmail", "v1", creds)
    assert google_service("gmail", "v1", creds)


def test2google_service1drive(creds):
    assert google_service("gmail", "v1", creds)
    assert google_service("gmail", "v1", creds)


def test2google_service_ex():
    assert google_service_ex(SCOPES_MAIL, "gmail", "v1")
    assert google_service_ex(SCOPES_DRIVE, "drive", "v3")


@pytest.fixture
def _clean():
    CRED_MAIL.unlink(missing_ok=True)
    yield None


@pytest.fixture
def creds():
    scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
    yield xauth(scopes, "gmail", "v1")

