#!/usr/bin/env python3


def gdrive_clean(service, query, names):
    from googleapiclient.http import MediaIoBaseDownload
    from gdrive_ls import gdrive_ls_ex
    from pathlib import Path

    total_size = 0
    for id, type, name in gdrive_ls_ex(service, query):
        try:
            permissions = (
                service.permissions()
                .list(fileId=id, fields="permissions(type)")
                .execute()
            )
        except Exception as e:
            print(f"error {e} '{name}'")
            continue
        is_globally_shared = False
        for permission in permissions.get("permissions", []):
            if permission["type"] == "anyone":
                is_globally_shared = True
                break

        if is_globally_shared:
            print(f"keep '{name}'")
        else:
            # グローバル共有されていない場合、ファイルを削除
            # service.files().delete(fileId=id).execute()
            try:
                file = service.files().get(fileId=id, fields="size").execute()
                size = int(file.get("size"))
            except Exception as e:
                print(f"unknown {e.__class__.__name__} '{name}'")
            else:
                if name in names:
                    print(f"name '{name}")
                else:
                    names.add(name)
                    print(f"move {size} '{name}'")
                    path = Path("~/Downloads/from-gdrive").expanduser() / name
                    request = service.files().get_media(fileId=id)
                    with path.open("wb") as oobj:
                        downloader = MediaIoBaseDownload(oobj, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print(f"ダウンロード進捗: {int(status.progress() * 100)}%")
                    service.files().delete(fileId=id).execute()
                total_size += size
    print(total_size / 1024 / 1024 / 1024)


def main():
    from xauth import google_service_ex
    from gdrive_ls import gdrive_ls_service

    service = google_service_ex(
        [
            "https://www.googleapis.com/auth/drive.file",
        ],
        "drive",
        "v3",
    )
    #service = gdrive_ls_service()
    for q in "mimeType contains 'audio/'", "mimeType contains 'video/'":
        gdrive_clean(service, q, set())


if __name__ == "__main__":
    main()
