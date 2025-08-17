import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path

secrets_dir = Path("~/Secrets")
credentials_json = secrets_dir / "gdrive-put.json"
credentials_json = credentials_json.expanduser()
here = Path(__file__).resolve().parent
token_json = here / "token.json"

# 認証スコープ
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    creds = None
    # token.json があれば認証情報をロード
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    # 認証情報がない場合、または期限切れの場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # 認証情報を保存
        with open(token_json, 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_file_to_drive(file_path):
    """
    指定されたファイルを Google Drive にアップロードし、パーマリンクを返す
    """
    creds = authenticate_google_drive()
    drive_service = build('drive', 'v3', credentials=creds)

    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)

    try:
        # ファイルをアップロード
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink, webContentLink'
        ).execute()

        file_id = uploaded_file.get('id')
        web_view_link = uploaded_file.get('webViewLink')

        # パーミッション設定: リンクを知っている全員が閲覧可能
        permission = {
            'type': 'anyone',
            'role': 'reader',
        }
        drive_service.permissions().create(
            fileId=file_id,
            body=permission,
            fields='id'
        ).execute()

        print(f"ファイル名: {file_name}")
        print(f"ファイルID: {file_id}")
        print(f"パーマリンク (閲覧用): {web_view_link}")
        
        return web_view_link
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

if __name__ == '__main__':
    # アップロードしたいファイルのパスを指定
    file_to_upload = 'example.txt' 
    # サンプルファイルを作成 (事前に作成しておくか、任意のファイルを指定)
    with open(file_to_upload, 'w') as f:
        f.write("これはテストファイルです。")
    
    upload_link = upload_file_to_drive(file_to_upload)
    if upload_link:
        print(f"アップロード成功！ 🚀")
        print(f"生成されたパーマリンク: {upload_link}")