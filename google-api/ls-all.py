def ls():
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    scopes = ["https://www.googleapis.com/auth/drive.file"]
    service = google_service_ex(scopes, "drive", "v3")

    query = "mimeType = 'audio/mpeg'"
    page_token = None
    kw = dict(
        q=query,
        fields="nextPageToken, files(name)",
    )
    while True:
        results = service.files().list(**kw, pageToken=page_token).execute()
        items = results.get("files", [])
        page_token = results.get("nextPageToken", None)
        yield from items
        if page_token is None:
            break


def main():
    for y in ls():
        print(y)


if __name__ == "__main__":
    main()
