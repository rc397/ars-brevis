import io
import os
import sys
import urllib.request
import zipfile

URL = "https://github.com/fchollet/ARC-AGI/archive/refs/heads/master.zip"


def main(dest):
    archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read()))
    root = archive.namelist()[0]
    training = os.path.join(dest, "training")
    os.makedirs(training, exist_ok=True)
    count = 0
    for name in archive.namelist():
        if name.startswith(root + "data/training/") and name.endswith(".json"):
            with open(os.path.join(training, os.path.basename(name)), "wb") as f:
                f.write(archive.read(name))
            count += 1
    license_name = root + "LICENSE"
    if license_name in archive.namelist():
        with open(os.path.join(dest, "LICENSE"), "wb") as f:
            f.write(archive.read(license_name))
    print(f"{count} tasks written to {training}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/arc")
