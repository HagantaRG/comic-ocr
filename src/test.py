import os
from pathlib import Path

from html_utils import Page, make_html_file

folder_path: str = "C:\\Users\\rhaga\\Documents\\test"
file_list: list[str] = os.listdir(folder_path)
file_list.sort(key=lambda fname: int(fname.split('.')[0]))
page_num = 0
page_batch: int = 5
batches: list = [[]]
manga: dict[int, Page] = {}
processing_files: list[str] = file_list
for num, file in enumerate(processing_files):
    path = Path(f"{folder_path}/{file}")
    manga[num + 1] = Page(
        img_filepath=path,
        page_num=num + 1,
        page_class="page"
    )

final_html: str = make_html_file(manga)
with open(f"{folder_path}/HELP.html", "w+", encoding="utf-8") as f:
    f.write(final_html)