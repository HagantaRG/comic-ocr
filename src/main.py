import os
from pathlib import Path
from threading import Thread
from typing import Final
from tqdm import tqdm

from easyocr import Reader
from manga_ocr import MangaOcr

from html_utils import Page, make_html_file
from functions import process_page
from filepaths import PROJECT_FOLDER

VALID_EXTENSIONS: Final[list[str]] = [
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tiff"
]

def main(
        folder_path: str,
        manga_name: str = ...
):
    path_folder: Path = Path(folder_path)
    file_list: list[str] = os.listdir(folder_path)
    file_list.sort(key=lambda fname: int(fname.split('.')[0]))
    page_num = 0
    manga: dict[int, Page] = {}
    manga_name: str = path_folder.name if manga_name is ... else manga_name
    print(f"Processing {manga_name}")
    for file in file_list:
        if file.split('.')[-1] in VALID_EXTENSIONS:
            pass
        else:
            raise TypeError(file)

    detector = Reader(
        lang_list=['ja'],
        recognizer=False,
        gpu=True
    )
    recogniser = MangaOcr()

    for file in tqdm(file_list):
        path = Path(f"{folder_path}/{file}")
        page_num += 1
        process_page(
            manga=manga,
            filepath=path,
            detector=detector,
            recogniser=recogniser,
            page_num=page_num
        )

    final_html: str = make_html_file(manga)
    if os.path.exists(f"{PROJECT_FOLDER}/outputs"):
        pass
    else:
        os.mkdir(f"{PROJECT_FOLDER}/outputs")
    with open(f"{PROJECT_FOLDER}/outputs/{manga_name}.html", "w+", encoding="utf-8") as f:
        f.write(final_html)
    print("Done")

while True:
    user_input: str = input(
        f"Hello! Please type in \"help\" to see a list of commands. Otherwise, please type in a valid command.\n"
    )
    user_input = user_input.strip()
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
                try:
                    main(target_folder)
                except TypeError as type_error:
                    print(f"One of the files in ({str(type_error)}) your target folder is an invalid filetype.")
        case _:
            print(
                """
That was not a valid command.
                """
            )
