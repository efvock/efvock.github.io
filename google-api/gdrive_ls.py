def gdrive_ls_service():
    from xauth import google_service_ex

    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    return google_service_ex(scopes, "drive", "v3")


def gdrive_ls(query):
    return gdrive_ls_ex(gdrive_ls_service(), query)


def gdrive_ls_ex(service, query):
    page_token = None
    while True:
        results = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
            )
            .execute()
        )

        items = results.get("files", [])
        page_token = results.get("nextPageToken", None)
        if page_token is None:
            break

        yield from ([y["id"], y["mimeType"], y["name"]] for y in items)


def main():
    from collections import defaultdict
    from pathlib import Path
    from googleapiclient.http import MediaIoBaseDownload

    infixes = defaultdict(int)
    suffixes = defaultdict(set)
    service = gdrive_ls_service()
    for q in "mimeType contains 'audio/'", "mimeType contains 'video/'":
        for id, type, name in gdrive_ls_ex(service, q):
            name = Path(name)
            assert name.parts.__len__() == 1
            v = suffixes[name.suffix]
            if not v:
                v.add(type)
            else:
                assert v.__len__() == 1
                assert type in v
            infixes[name] += 1
            if infixes[name] != 1:
                name = f"{name.stem}-{infixes[name]}{name.suffix}"
                name = Path(name)
            path = "/tmp/from-gdrive" / name
            request = service.files().get_media(fileId=id)
            with path.open("wb") as oobj:
                downloader = MediaIoBaseDownload(oobj, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"ダウンロード進捗: {int(status.progress() * 100)}%")
    _ = 0


if __name__ == "__main__":
    main()
