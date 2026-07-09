import os
from datetime import datetime, timedelta

from PIL import Image, ImageDraw
from easyocr import Reader
from manga_ocr import MangaOcr

from html_utils import Textbox, Page, make_html_file
from img_utils import merge_textboxes_easyocr

detector = Reader(
    lang_list=['ja'],
    recognizer=False
)

recogniser = MangaOcr()
region_count: int = 0
final_html: str = ""
pages: list[Page] = []
file_list: list[str] = os.listdir("test-pics/temporary")
file_list.sort(key=lambda fname: int(fname.split('.')[0]))
page_num = 0
for file in file_list[4:6]:
    filepath = f"test-pics/temporary/{file}"
    print(f"Processing {filepath}")
    page_num += 1
    result = detector.detect(filepath)
    with Image.open(filepath) as img:
        width, height = img.size
        drawer = ImageDraw.Draw(img)
        count: int = 0
        print(f"Image is {width}x{height}")
        page: Page = Page(
            img_filepath=f"{filepath}",
            page_num=page_num,
            page_class="page"
        )
        pages.append(page)
        print(f"Merging regions...")
        start = datetime.now()
        merged_regions: list[list[int]] = merge_textboxes_easyocr(result[0][0])
        end = datetime.now()
        delta: timedelta = end - start
        print(f"Merging took {delta.total_seconds()} for page {page_num}")
        for item in merged_regions:
            count += 1
            nums: list[float] = []
            for np_num in item:
                nums.append(float(np_num))
            region_list = [nums[0],nums[2],nums[1],nums[3]]
            box_width: float =  nums[1] - nums[0]
            box_height: float = nums[3] - nums[2]
            percent_width: int = int(box_width / width * 100)
            percent_height: int = int(box_height / height * 100)
            drawer.rectangle(region_list, outline='red')
            region = img.crop((nums[0],nums[2],nums[1],nums[3]))
            text: str = recogniser(region)
            textbox: Textbox = Textbox(
                top=int(nums[2]/height*100),
                left=int(nums[0]/width*100),
                height=percent_height,
                width=percent_width,
                text=text
            )
            page.textboxes.append(textbox)
        print(f"Done with page {page_num}")
    img.save(f'outputs/test-ocr-{page_num}.png')
    print(f"Image saved to outputs/test-ocr-{page_num}.png")

final_html = make_html_file(pages)
with open("HELP.html", "w", encoding="utf-8") as f:
    f.write(final_html)