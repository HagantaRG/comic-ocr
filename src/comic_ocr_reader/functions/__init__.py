from datetime import datetime
from pathlib import Path

from PIL import Image
from easyocr import Reader
from manga_ocr import MangaOcr

from comic_ocr_reader.html_utils import Textbox, Page
from comic_ocr_reader.img_utils import merge_textboxes_easyocr

def process_page(
        manga: dict[int, Page],
        filepath: Path,
        detector: Reader,
        recogniser: MangaOcr,
        page_num: int
) -> None:

    result = detector.detect(str(filepath))
    with Image.open(filepath) as img:
        textboxes: list[Textbox] = []
        width, height = img.size

        count: int = 0
        page: Page = Page(
            img_filepath=f"{filepath.stem}{filepath.suffix}",
            page_num=page_num,
            page_class="page"
        )
        merged_regions: list[list[int]] = merge_textboxes_easyocr(
            result[0][0],
            padding=1
        )
        for item in merged_regions:
            count += 1
            nums: list[int] = []
            for np_num in item:
                nums.append(int(np_num))

            box_width: int = nums[1] - nums[0]
            box_height: int = nums[3] - nums[2]
            percent_width: int = round(box_width / width * 100)
            percent_height: int = round(box_height / height * 100)

            region = img.crop((nums[0], nums[2], nums[1], nums[3]))
            start = datetime.now()
            text: str = recogniser(region)
            end = datetime.now()
            textbox: Textbox = Textbox(
                top=round(nums[2] / height * 100),
                left=round(nums[0] / width * 100),
                height=int(percent_height),
                width=int(percent_width),
                text=text
            )
            textboxes.append(textbox)
            page.textboxes = textboxes
        manga[page_num] = page
