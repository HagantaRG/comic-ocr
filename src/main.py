import os
from pathlib import Path
from datetime import datetime, timedelta
from threading import Thread

from easyocr import Reader
from manga_ocr import MangaOcr

from html_utils import Page, make_html_file
from functions import process_page

start = datetime.now()
detector = Reader(
    lang_list=['ja'],
    recognizer=False
)
recogniser = MangaOcr()
end = datetime.now()
delta: timedelta = end - start
print(f"Loading OCR models took {delta.total_seconds()} seconds")

region_count: int = 0
final_html: str = ""
file_list: list[str] = os.listdir("test-pics/temporary")
file_list.sort(key=lambda fname: int(fname.split('.')[0]))
page_num = 0

threads: list[Thread] = []
manga: list[Page] = []
for file in file_list[9:12]:
    path = Path(f"test-pics/temporary/{file}")
    page_num += 1
    thread: Thread = Thread(
        target=process_page,
        kwargs={
            "manga": manga,
            "filepath": path,
            "detector": detector,
            "recogniser": recogniser,
            "page_num": page_num
        }
    )
    threads.append(thread)

for t in threads:
    t.start()
for t in threads:
    t.join()

final_html = make_html_file(manga)
with open("./HELP.html", "w", encoding="utf-8") as f:
    f.write(final_html)

