#운영체제파일정보.py

import os
import glob
import shutil
from pathlib import Path

print(os.name)
print(os.environ)

fName = r"c://python313//python.exe"
if os.path.exists(fName):
    print(f"{fName} file exists: {os.path.getsize(fName)} bytes")
else: 
    print(f"{fName} file does not exist")

print(os.path.abspath("demo.txt"))
print(os.path.basename(r"c:\work\demo.txt"))

print(glob.glob(r"c:\work\*.py"))
for item in glob.glob(r"c:\work\*.8"):
    print(item)


def sort_downloads():
    downloads = Path(r"C:\Users\student\Downloads")
    folders = {
        "images": {".jpg", ".jpeg"},
        "data": {".csv", ".xlsx"},
        "docs": {".txt", ".doc", ".pdf"},
        "archive": {".zip"},
    }

    for folder in folders:
        (downloads / folder).mkdir(exist_ok=True)

    for source in downloads.iterdir():
        if not source.is_file():
            continue

        destination_folder = next(
            (folder for folder, extensions in folders.items()
             if source.suffix.lower() in extensions),
            None,
        )
        if destination_folder is None:
            continue

        destination = downloads / destination_folder / source.name
        if destination.exists():
            print(f"Skipped (already exists): {destination}")
            continue

        shutil.move(str(source), str(destination))
        print(f"Moved: {source.name} -> {destination_folder}")


if __name__ == "__main__":
    sort_downloads()


