def gdrive_put(localname, remotename):
    """
    >>> gdrive_put("null.docx", "pork.docx").startswith("https://")
    True
    """
    service = gdrive_put_service()
    return gdrive_put_ex(service, [(localname, remotename)]).__next__()


def gdrive_put_service():
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/drive.file"]
    return google_service_ex(scopes, "drive", "v3")



def gdrive_put_ex(service, g):
    from pathlib import Path
    from googleapiclient.http import MediaFileUpload

    for localname, remotename in g:
        metadata = {"name": remotename}
        media = MediaFileUpload(localname, resumable=True)

        uploaded = (
            service.files()
            .create(
                body=metadata,
                media_body=media,
                fields="id, webViewLink",
            )
            .execute()
        )

        id = uploaded.get("id")
        web_view_link = uploaded.get("webViewLink")

        # パーミッション設定: リンクを知っている全員が閲覧可能
        permission = {
            "type": "anyone",
            "role": "commenter",
        }
        service.permissions().create(fileId=id, body=permission, fields="id").execute()

        yield web_view_link


if __name__ == "__main__":
    from doctest import testmod

    testmod()
