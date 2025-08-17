"""
>>> SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
>>> creds = xauth(SCOPES)
>>> bool(google_service("gmail", "v1", creds))
True
>>> bool(google_service("gmail", "v1", creds))
True
>>> bool(google_service_ex(SCOPES, "gmail", "v1"))
True

>>> SCOPES = ["https://www.googleapis.com/auth/drive.file"]
>>> bool(google_service_ex(SCOPES, "drive", "v3"))
True
"""

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow as AppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path

secrets_dir = Path("~/Secrets").expanduser()
credentials_json = secrets_dir / "credentials.json"
here = Path(__file__).resolve().parent
token_json = (secrets_dir / here.name).with_suffix(".json")

def xauth(scopes):
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
    return build(service, version, credentials=creds)


def google_service_ex(scope, service, version):
    creds = xauth(scope)
    return google_service(service, version, creds)


if __name__ == "__main__":
    from doctest import testmod
    testmod()
