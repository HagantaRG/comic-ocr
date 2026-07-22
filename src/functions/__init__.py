import os
from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw
from easyocr import Reader
from manga_ocr import MangaOcr

from src.html_utils import Textbox, Page, make_html_file
from src.img_utils import merge_textboxes_easyocr

def process_page(
        manga: list[Page],
        filepath: Path,
        detector: Reader,
        recogniser: MangaOcr,
        page_num: int
) -> None:
    start = datetime.now()
    result = detector.detect(str(filepath))
    end = datetime.now()
    delta: timedelta = end - start
    print(f"Detection took {delta.total_seconds()}s for page {page_num}")
    with Image.open(filepath) as img:
        textboxes: list[Textbox] = []
        width, height = img.size

        count: int = 0
        page: Page = Page(
            img_filepath=f"{filepath}",
            page_num=page_num,
            page_class="page"
        )
        merged_regions: list[list[int]] = merge_textboxes_easyocr(
            result[0][0],
            padding=int(height * 0.01)
        )
        recog_time: delta = timedelta(seconds=0)
        for item in merged_regions:
            count += 1
            nums: list[int] = []
            for np_num in item:
                nums.append(int(np_num))

            box_width: int = nums[1] - nums[0]
            box_height: int = nums[3] - nums[2]
            percent_width: int = round(box_width / width * 100)
            percent_height: int = round(box_height / height * 100)
            # drawer = ImageDraw.Draw(img)
            # region_list = [nums[0], nums[2], nums[1], nums[3]]
            # drawer.rectangle(region_list, outline='red')
            region = img.crop((nums[0], nums[2], nums[1], nums[3]))
            start = datetime.now()
            text: str = recogniser(region)
            end = datetime.now()
            recog_time += end - start
            textbox: Textbox = Textbox(
                top=round(nums[2] / height * 100),
                left=round(nums[0] / width * 100),
                height=int(percent_height),
                width=int(percent_width),
                text=text
            )
            textboxes.append(textbox)
            page.textboxes = textboxes
        print(f"Recog took {recog_time.total_seconds()}s for page {page_num}")
        manga.append(page)
