import os
from pathlib import Path
from typing import Final
from tqdm import tqdm
from loguru import logger

from easyocr import Reader
from manga_ocr import MangaOcr

from comic_ocr_reader.html_utils import Page, make_html_file
from comic_ocr_reader.functions import process_page
from comic_ocr_reader.functions.model_init import ensure_models_initialised

VALID_EXTENSIONS: Final[list[str]] = [
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tiff"
]
logger.disable("manga_ocr")


def print_main_menu() -> None:
    print(
        'Hello! Please type in "help" to see a list of commands. '
        'Otherwise, please type in a valid command.'
    )


def main(
        folder_path: str,
        manga_name: str = ...
) -> bool:
    path_folder: Path = Path(folder_path)
    file_list: list[str] = os.listdir(path_folder)
    images: list[str] = []
    page_num = 0
    manga: dict[int, Page] = {}
    manga_name: str = path_folder.name if manga_name is ... else manga_name
    print(f"Processing the folder of manga titled \"{manga_name}\"")
    for file in file_list:
        if Path(f"{path_folder}/{file}").is_file():
            if file.split('.')[-1] in VALID_EXTENSIONS:
                images.append(file)
            else:
                continue
        else:
            continue
    print(f"Found {len(images)} pages in folder.")
    try:
        images.sort(key=lambda fname: int(fname.split('.')[0]))
    except ValueError:
        print("One of the image files in the folder you have entered has a non-integer name. (e.g. 123abc.jpeg instead of 123.jpeg)\n"
              "All image files within the folder *must* have an integer name for ordering purposes.")
        return False

    print("=== Initialisation ===")
    ensure_models_initialised()

    print("=== OCR setup ===")
    detector = Reader(
        lang_list=['ja'],
        recognizer=False,
        gpu=True
    )
    recogniser = MangaOcr()

    print("=== OCR processing ===")
    for file in tqdm(images):
        page_num += 1
        process_page(
            manga=manga,
            filepath=Path(f"{folder_path}/{file}"),
            detector=detector,
            recogniser=recogniser,
            page_num=page_num
        )

    final_html: str = make_html_file(manga)
    with open(f"{folder_path}/{manga_name}.html", "w+", encoding="utf-8") as f:
        f.write(final_html)
        f.flush()
    return True


def run() -> None:
    while True:
        try:
            print_main_menu()
            user_input: str = input().strip().lower()
            match user_input:
                case "help":
                    print(
                        """
        The valid commands are:
        - folder
            Allows you to specify a folder containing the image files for the manga you want to process.
            Also optionally allows you to give the manga a name. Otherwise the folder name will be used.
            Supported file formats for images in folder: .jpg, .jpeg, .png, .bmp, .tiff
        And of course,
        - help
            Which you are currently using.
                        """
                    )
                case "folder":
                    target_folder: str = input("Please input a target folder.\n")
                    if os.path.isdir(target_folder):
                        if main(target_folder):
                            print("Success! Returning to the main menu.")
                        else:
                            print("Something went wrong. Returning to the main menu.")
                    else:
                        print("Please input a valid folder. Returning to the main menu.")
                case _:
                    print("That was not a valid command. Returning to the main menu.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return


if __name__ == "__main__":
    run()
