from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Callable, Optional

from easyocr import Reader
from easyocr.config import MODULE_PATH as EASYOCR_MODULE_PATH, detection_models as EASYOCR_DETECTION_MODELS
from manga_ocr import MangaOcr

EASYOCR_DETECTOR_NAME = "craft"
EASYOCR_DETECTOR_MODEL = Path(EASYOCR_MODULE_PATH) / "model" / EASYOCR_DETECTION_MODELS[EASYOCR_DETECTOR_NAME]["filename"]

MANGA_OCR_REPO = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--kha-white--manga-ocr-base"
)
MANGA_OCR_REQUIRED_FILES = (
    "config.json",
    "preprocessor_config.json",
    "pytorch_model.bin",
    "special_tokens_map.json",
    "tokenizer_config.json",
    "vocab.txt",
)


def _file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def easyocr_detector_is_initialised(model_path: Path = EASYOCR_DETECTOR_MODEL) -> bool:
    expected_md5 = EASYOCR_DETECTION_MODELS[EASYOCR_DETECTOR_NAME]["md5sum"]
    return model_path.is_file() and _file_md5(model_path) == expected_md5


def manga_ocr_is_initialised(repo_path: Path = MANGA_OCR_REPO) -> bool:
    refs_main = repo_path / "refs" / "main"
    if not refs_main.is_file():
        return False

    snapshot_hash = refs_main.read_text(encoding="utf-8").strip()
    if not snapshot_hash:
        return False

    snapshot_dir = repo_path / "snapshots" / snapshot_hash
    if not snapshot_dir.is_dir():
        return False

    return all((snapshot_dir / filename).is_file() for filename in MANGA_OCR_REQUIRED_FILES)


def models_are_initialised(
    easyocr_model_path: Path = EASYOCR_DETECTOR_MODEL,
    manga_repo_path: Path = MANGA_OCR_REPO,
) -> bool:
    return easyocr_detector_is_initialised(easyocr_model_path) and manga_ocr_is_initialised(manga_repo_path)


def _download_easyocr_detector() -> None:
    Reader(lang_list=["ja"], recognizer=False, gpu=True, detect_network=EASYOCR_DETECTOR_NAME)


def _download_manga_ocr() -> None:
    MangaOcr()


def ensure_models_initialised(
    easyocr_model_path: Path = EASYOCR_DETECTOR_MODEL,
    manga_repo_path: Path = MANGA_OCR_REPO,
    easyocr_factory: Optional[Callable[[], None]] = None,
    manga_factory: Optional[Callable[[], None]] = None,
) -> bool:
    if models_are_initialised(easyocr_model_path, manga_repo_path):
        print("Not required! You have already initialised.")
        return False

    if not easyocr_detector_is_initialised(easyocr_model_path):
        (easyocr_factory or _download_easyocr_detector)()

    if not manga_ocr_is_initialised(manga_repo_path):
        (manga_factory or _download_manga_ocr)()

    print("Initialisation complete.")
    return True
