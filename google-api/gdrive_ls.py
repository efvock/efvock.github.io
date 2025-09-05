def gdrive_ls_service():
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    return google_service_ex(scopes, "drive", "v3")


def gdrive_ls(query):
    return gdrive_ls_ex(gdrive_ls_service(), query)


def gdrive_ls_ex(service, query):
    """Google Drive内のすべての音声ファイルを見つけて、そのIDをリストします。"""
    audio_files = []
    page_token = None
    while True:
        results = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
            )
            .execute()
        )

        items = results.get("files", [])
        audio_files.extend(items)
        page_token = results.get("nextPageToken", None)
        if page_token is None:
            break

    if not audio_files:
        return

    for file in audio_files:
        yield file["id"], file["name"]


def main():
    service = gdrive_ls_service()
    for q in "mimeType = 'audio/mpeg'", "mimeType contains 'audio/'":
        for y in gdrive_ls_ex(service, q):
            print(*y)


if __name__ == "__main__":
    main()
