from pathlib import Path
from datetime import datetime
import mimetypes

from utils.hashing import calculate_hashes


def analyze_file(file_path: str) -> dict:
    """
    Perform basic forensic analysis on any file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    stat = path.stat()

    hashes = calculate_hashes(file_path)

    mime_type, _ = mimetypes.guess_type(file_path)

    result = {
        "file_name": path.name,
        "file_extension": path.suffix.lower(),
        "file_size_bytes": stat.st_size,
        "file_size_kb": round(stat.st_size / 1024, 2),
        "mime_type": mime_type or "unknown",
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
        "md5": hashes["md5"],
        "sha256": hashes["sha256"],
    }

    return result
