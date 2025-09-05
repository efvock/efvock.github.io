"""
>>> SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
>>> creds = xauth(SCOPES, "gmail", "v1")
>>> bool(google_service("gmail", "v1", creds))
True

>>> bool(google_service("gmail", "v1", creds))
True

>>> bool(google_service_ex(SCOPES, "gmail", "v1"))
True

>>> SCOPES = ["https://www.googleapis.com/auth/drive.file"]
>>> bool(google_service_ex(SCOPES, "drive", "v3"))
True

>>> SCOPES = ["https://x.com/ab/c.d", "file:///pq/r.s"]
>>> cred_cache(SCOPES, "drive", "v3")
'google-api_drive_v3_ab-c.d--pq-r.s'
"""

from pathlib import Path

SECRETS_DIR = Path("~/Secrets").expanduser()


def cred_cache_path(scopes, name, version):
    y = f"{SECRETS_DIR / cred_cache(scopes, name, version)}.json"
    return Path(y)

def cred_cache(scopes, name, version):
    from pathlib import Path
    from urllib.parse import urlparse

    here = Path(__file__).resolve().parent
    expanded_scopes = (urlparse(y).path for y in scopes)
    expanded_scopes = map(Path, expanded_scopes)
    expanded_scopes = "--".join("-".join(y.parts[1:]) for y in expanded_scopes)
    return f"{here.stem}_{name}_{version}_{expanded_scopes}"


def xauth(scopes, name, version):
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow as AppFlow
    from google.oauth2.credentials import Credentials

    credentials_json = SECRETS_DIR / "credentials.json"
    token_json = cred_cache_path(scopes, name, version)
    creds = None
    if token_json.exists():
        creds = Credentials.from_authorized_user_file(token_json, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = AppFlow.from_client_secrets_file(credentials_json, scopes)
            creds = flow.run_local_server(port=0)
        token_json.write_text(creds.to_json())
    return creds


def google_service(service, version, creds):
    from googleapiclient.discovery import build

    return build(service, version, credentials=creds)


def google_service_ex(scope, service, version):
    creds = xauth(scope, service, version)
    return google_service(service, version, creds)
