#!/usr/bin/env python3


def main():
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
    service = google_service_ex(scopes, "gmail", "v1")
    save(service, "from:me to:me")


def save(service, query, output_file='headers.txt'):
    """アーカイブされたメッセージのヘッダーを取得し、ファイルに保存する"""
    # 'in:archive' でアーカイブされたメッセージを検索
    search_results = service.users().messages().list(userId='me', q=f'{query} in:archive').execute()
    messages = search_results.get('messages', [])

    if not messages:
        print("指定された条件に一致するアーカイブ済みメッセージは見つかりませんでした。")
        return

    # 最初に見つかったメッセージのIDを取得
    message_id = messages[0]['id']
    print(f"メッセージID {message_id} のヘッダーを取得します。")

    # メッセージ全体を取得
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    headers = msg['payload']['headers']

    with open(output_file, 'w', encoding='utf-8') as f:
        for header in headers:
            f.write(f"{header['name']}: {header['value']}\n")
    
    print(f"ヘッダーが {output_file} に保存されました。")


if __name__ == '__main__':
    main()
