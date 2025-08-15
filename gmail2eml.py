#!/usr/bin/python3

from base64 import urlsafe_b64decode
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path

secrets_dir = Path("~/Secrets").expanduser()
credentials_json = secrets_dir / "credentials.json"
here = Path(__file__).resolve().parent
token_json = here / "token.json"
emls = here / "emls"

# スコープ: Gmailのメールを読み取るための権限
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Google認証を行い、Gmail APIサービスオブジェクトを返します。"""
    creds = None
    # 'token.json' は、以前の実行で保存されたユーザーの認証情報を格納します。
    if token_json.exists():
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
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
    return build('gmail', 'v1', credentials=creds)

def save_emails_by_query(query, save_path=emls):
    """
    Gmailの検索クエリに基づいてメールを検索し、指定したディレクトリに.eml形式で保存します。
    """
    service = get_gmail_service()
    
    emls.mkdir(exist_ok=True)
    
    # 検索クエリに基づいてメールIDを取得
    response = service.users().messages().list(userId='me', q=query).execute()
    messages = response.get('messages', [])

    if not messages:
        print("指定された条件に一致するメールは見つかりませんでした。")
        return

    print(f"{len(messages)}件のメールが見つかりました。")

    for message in messages:
        # 各メールの完全な内容を取得
        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
        
        # 'raw'フォーマットはbase64でエンコードされているためデコード
        msg_raw_decoded = urlsafe_b64decode(msg['raw'].encode('ASCII'))
        
        # Message-IDを取得
        message_id = None
        for header in service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Message-ID']).execute()['payload']['headers']:
            if header['name'] == 'Message-ID':
                # <>を取り除く
                message_id = header['value'].strip('<>')
                break
        
        if message_id:
            body = get_message_body(get_gmail_service(), "me", message_id)
            (emls / message_id).with_suffix(".eml").write_bytes(body)
        else:
            print(f"メールID: {message['id']} のMessage-IDが見つかりませんでした。スキップします。")


import base64

def get_message_body(service, user_id, msg_id):
    """
    指定されたメッセージIDの本文を抽出します。
    """
    try:
        # メッセージの詳細を取得
        msg = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = msg['payload']
        parts = payload.get('parts')

        # 本文部分を探す
        if parts:
            for part in parts:
                mime_type = part.get('mimeType')
                if mime_type == 'text/plain' or mime_type == 'text/html':
                    # Base64でエンコードされたデータを取得
                    data = part['body'].get('data')
                    if data:
                        # URLセーフなBase64をデコード
                        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                        return decoded_data

        # parts がない場合、bodyから直接取得を試みる
        else:
            body = payload.get('body')
            if body and body.get('data'):
                decoded_data = base64.urlsafe_b64decode(body.get('data')).decode('utf-8')
                return decoded_data

        return "本文が見つかりませんでした。"
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

# 使用例（service, user_id, msg_id は適切な値に置き換えてください）
# body_content = get_message_body(service, 'me', 'メッセージID')
# print(body_content)

if __name__ == '__main__':
    # ユーザーの要求に合わせた検索クエリ
    search_query = 'from:viewcard@mail.viewsnet.jp subject:確報版'
    save_emails_by_query(search_query)