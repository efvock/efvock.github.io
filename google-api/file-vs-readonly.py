def case(scopes):
    from xauth import google_service_ex

    service = google_service_ex(scopes, "drive", "v3")

    query = "mimeType = 'audio/mpeg'"
    page_token = None
    list_params = dict(
        q=query,
        fields="nextPageToken, files(name)",
        pageToken=page_token,
    )
    while True:
        results = service.files().list(**list_params).execute()
        items = results.get("files", [])
        page_token = results.get("nextPageToken", None)
        yield from items
        if page_token is None:
            break


def main():
    file = ["https://www.googleapis.com/auth/drive.file"]
    ro = ["https://www.googleapis.com/auth/drive.readonly"]
    for y in case(file):
        print(y)
    for y in case(ro):
        print(y)


if __name__ == "__main__":
    main()
