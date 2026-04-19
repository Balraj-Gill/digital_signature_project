import os

from config import KEY_DIR, DOC_DIR, SIG_DIR


def ensure_directories():
    """
    Ensure all required project directories exist.
    """
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(DOC_DIR, exist_ok=True)
    os.makedirs(SIG_DIR, exist_ok=True)


def file_exists(path):
    """
    Check if a file exists.
    """
    return os.path.exists(path)


def read_bytes(path):
    """
    Read file as bytes.
    """
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path, data):
    """
    Write bytes to file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def get_filename(path):
    """
    Extract filename from path.
    """
    return os.path.basename(path)


def require_files(paths, label="file"):
    """
    Check that all required files exist.

    Args:
        paths (list[str]): File paths to check
        label (str): Label used in error output

    Returns:
        bool: True if all files exist, False otherwise
    """
    for path in paths:
        if not file_exists(path):
            print(f"Error: Required {label} not found -> {path}")
            return False
    return True