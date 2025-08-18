#!/usr/bin/env python3
import base64
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def save(
    service, output_headers="headers.txt", output_body="body.txt"
):
    """
    アーカイブされたメッセージを検索し、text/plainに変換できるメッセージを保存する。
    Args:
        service: 認証済みのGmail APIサービスオブジェクト。
        output_headers: ヘッダーを保存するファイル名。
        output_body: 本文を保存するファイル名。
    """
    try:
        profile = service.users().getProfile(userId='me').execute()
        
        # 'emailAddress'フィールドからメールアドレスを取得
        email = profile.get('emailAddress')
        # Step 1: アーカイブされたメッセージを検索
        # 'in:archive' クエリを使用してアーカイブ内のすべてのメッセージをリストアップ
        # 1件のみ取得するため、maxResults=1を設定
        search_results = (
            service.users()
            .messages()
            .list(userId="me", q=f"in:archive to:{email} from:{email}", maxResults=1)
            .execute()
        )
        messages = search_results.get("messages", [])

        if not messages:
            print("アーカイブされたメッセージが見つかりませんでした。")
            return

        message_id = messages[0]["id"]
        print(f"アーカイブされたメッセージ (ID: {message_id}) を取得します。")

        # Step 2: メッセージの完全な内容を取得
        # format='full' を使用して、ヘッダーと本文の情報をすべて取得
        message = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        payload = message["payload"]

        # Step 3: ヘッダーと本文の抽出とデコード
        # ヘッダーを抽出
        headers = payload.get("headers", [])

        # 本文のtext/plainパートを探す
        body_content = ""
        # is_text_plain_found = False

        # マルチパートメッセージかどうかのチェック
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data")
                    if data:
                        # Base64URLデコード
                        decoded_data = base64.urlsafe_b64decode(data).decode("utf-8")
                        body_content = decoded_data
                        # is_text_plain_found = True
                        break
        # シングルパートメッセージの場合
        elif payload["mimeType"] == "text/plain":
            data = payload["body"].get("data")
            if data:
                decoded_data = base64.urlsafe_b64decode(data).decode("utf-8")
                body_content = decoded_data
                # is_text_plain_found = True

        if not body_content:
            print("メッセージの本文にtext/plainパートが見つかりませんでした。")
            return

        # Step 4: ファイルに保存
        with open(output_headers, "w", encoding="utf-8") as f:
            for header in headers:
                f.write(f"{header['name']}: {header['value']}\n")

        print(f"ヘッダーが '{output_headers}' に保存されました。")

        with open(output_body, "w", encoding="utf-8") as f:
            f.write(body_content)

        print(f"本文が '{output_body}' に保存されました。")

    except HttpError as error:
        print(f"Gmail APIからエラーが発生しました: {error}")


def main():
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
    service = google_service_ex(scopes, "gmail", "v1")
    save(service)


if __name__ == "__main__":
    main()
