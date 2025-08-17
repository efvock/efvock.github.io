#!/usr/bin/env python3

"""
>>> SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
>>> bool(get_service(SCOPES, "gmail", "v1"))
True
>>> SCOPES = ["https://www.googleapis.com/auth/drive.file"]
>>> bool(get_service(SCOPES, "drive", "v3"))
True
"""

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path

secrets_dir = Path("~/Secrets").expanduser()
credentials_json = secrets_dir / "credentials.json"
here = Path(__file__).resolve().parent
token_json = here / "token.json"

def get_service(scopes, service, version):
    """Google認証を行い、Gmail APIサービスオブジェクトを返します。"""
    creds = None
    # 'token.json' は、以前の実行で保存されたユーザーの認証情報を格納します。
    if token_json.exists():
        creds = Credentials.from_authorized_user_file(token_json, scopes)
    # 有効な認証情報がない場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # 次回のために認証情報を保存します
        with token_json.open('w') as token:
            token.write(creds.to_json())
    return build(service, version, credentials=creds)

if __name__ == "__main__":
    from doctest import testmod
    testmod()
