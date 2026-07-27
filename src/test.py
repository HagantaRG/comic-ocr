import os
from pathlib import Path

from html_utils import Page, make_html_file

file_list: list[str] = os.listdir("test-pics/temporary")
file_list.sort(key=lambda fname: int(fname.split('.')[0]))
page_num = 0
page_batch: int = 5
batches: list = [[]]
manga: dict[int, Page] = {}
processing_files: list[str] = file_list[2:8]
for num, file in enumerate(processing_files):
    path = Path(f"test-pics/temporary/{file}")
    manga[num + 1] = Page(
        img_filepath=path,
        page_num=num + 1,
        page_class="page"
    )

final_html: str = make_html_file(manga)
with open("./HELP.html", "w", encoding="utf-8") as f:
    f.write(final_html)