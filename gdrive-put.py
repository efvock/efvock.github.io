def upload_file_to_drive(file_path):
    from xauth import google_service
    from googleapiclient.http import MediaFileUpload
    from pathlib import Path
    scopes = ["https://www.googleapis.com/auth/drive.file"]
    """
    指定されたファイルを Google Drive にアップロードし、パーマリンクを返す
    """
    service = google_service(scopes, "drive", "v3")
    
    file_name = Path(file_path).name
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)

    try:
        # ファイルをアップロード
        uploaded_file = service.files().create(
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
        service.permissions().create(
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