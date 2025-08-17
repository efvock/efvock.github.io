def gdrive_put(file_path):
    """
    >>> gdrive_put("/dev/null").startswith("https://")
    True
    """
    from os.path import devnull
    from pathlib import Path
    from googleapiclient.http import MediaFileUpload
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/drive.file"]
    service = google_service_ex(scopes, "drive", "v3")
    
    file_metadata = {"name": "beef.docx"}
    media = MediaFileUpload(devnull, resumable=True)

    uploaded_file = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink, webContentLink",
        )
        .execute()
    )

    file_id = uploaded_file.get("id")
    web_view_link = uploaded_file.get("webViewLink")
    l = uploaded_file.get("webContentLink")

    # パーミッション設定: リンクを知っている全員が閲覧可能
    permission = {
        "type": "anyone",
        "role": "commenter",
    }
    service.permissions().create(
        fileId=file_id, body=permission, fields="id"
    ).execute()

    return web_view_link


if __name__ == "__main__":
    from doctest import testmod
    testmod()
