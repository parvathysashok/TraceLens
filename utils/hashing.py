import hashlib
from pathlib import Path


def calculate_hashes(file_path: str) -> dict:
    """
    Calculate cryptographic hashes for a file.
    """

    path = Path(file_path)

    md5 = hashlib.md5()
    sha256 = hashlib.sha256()

    with open(path, "rb") as file:
        while chunk := file.read(1024 * 1024):
            md5.update(chunk)
            sha256.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha256": sha256.hexdigest(),
    }
