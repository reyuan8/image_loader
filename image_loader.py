#!/usr/bin/env python3

import concurrent.futures
import pathlib
import argparse
import typing

import requests


TARGET_URL = "http://127.0.0.1:8000/users/1/upload-avatar/"
TARGET_FIELD = "avatar"
EXTENSIONS = ["jpg", "jpeg", "png", "tiff", "bmp", "gif"]


def upload_file(filepath, url, url_field):
    response = requests.post(url, files={url_field: open(filepath, "rb")})
    if response.ok:
        print(f"{pathlib.Path(filepath).name} uploaded successfully.")
    else:
        print(f"{pathlib.Path(filepath).name} was not uploaded.")


def get_files_by_extensions(
    path: str, extensions: typing.List[str]
) -> typing.List[str]:
    files_path = pathlib.Path(path)

    matched_files = []

    for extension in extensions:
        matched_files.extend(files_path.glob(f"*.{extension}"))

    return [str(f.absolute()) for f in matched_files]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Enter images path.")
    args = parser.parse_args()

    files = get_files_by_extensions(args.path, EXTENSIONS)

    uploads = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for file in files:
            uploads.append(
                executor.submit(upload_file, file, TARGET_URL, TARGET_FIELD),
            )
        concurrent.futures.wait(uploads)
        print("All files uploaded successfully.")


if __name__ == "__main__":
    main()
