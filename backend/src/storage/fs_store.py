import os
from pathlib import Path


BASE_UPLOAD_DIR = Path("C:/Users/Tcyber/Documents/PROJECTS/LlamaInde-Chatbot/data/uploads")


def ensure_upload_dir():
    BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_upload(filename: str, content: bytes) -> str:
    ensure_upload_dir()
    target = BASE_UPLOAD_DIR / filename
    with open(target, "wb") as f:
        f.write(content)
    return str(target.resolve())
