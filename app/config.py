import os

from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_abs_path(file_path: str) -> str:
    """append ROOT_DIR for relative path"""
    # Already absolute path
    if file_path.startswith("/"):
        return file_path
    else:
        return os.path.join(ROOT_DIR, file_path)


config_file = os.environ.get("CONFIG")

# config file check
if config_file:
    config_file = get_abs_path(config_file)
    print("load config file", config_file)
    load_dotenv(get_abs_path(config_file))
else:
    load_dotenv()

# Database
DB_CONNECTION_STRING = os.environ["DB_CONNECTION_STRING"]
STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_KEY = os.environ.get("STORAGE_ACCOUNT_KEY")
STORAGE_CONTAINER = os.environ.get("STORAGE_CONTAINER")
