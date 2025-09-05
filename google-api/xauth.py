"""
>>> SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
>>> creds = yauth(SCOPES, "gmail", "v1")
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


def yauth(scopes, name, version):
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow as AppFlow
    from google.oauth2.credentials import Credentials
    from pathlib import Path
    from urllib.parse import urlparse

    secrets_dir = Path("~/Secrets").expanduser()
    credentials_json = secrets_dir / "credentials.json"
    here = Path(__file__).resolve().parent
    expanded_scopes = (urlparse(y).path for y in scopes)
    expanded_scopes = map(Path, expanded_scopes)
    expanded_scopes = "-".join("-".join(y.parts[1:]) for y in expanded_scopes)
    cache = f"{here.stem}_{name}_{version}_{expanded_scopes}"
    token_json = (secrets_dir / cache).with_suffix(".json")

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
    creds = yauth(scope, service, version)
    return google_service(service, version, creds)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
