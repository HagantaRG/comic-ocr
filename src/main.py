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
for file in file_list[8:10]:
    filepath = f"test-pics/temporary/{file}"
    print(f"Processing {filepath}")
    page_num += 1
    result = detector.detect(filepath)
    with Image.open(filepath) as img:
        textboxes: list[Textbox] = []
        width, height = img.size
        drawer = ImageDraw.Draw(img)
        count: int = 0
        page: Page = Page(
            img_filepath=f"{filepath}",
            page_num=page_num,
            page_class="page"
        )
        pages.append(page)
        print(f"Merging regions...")
        start = datetime.now()
        merged_regions: list[list[int]] = merge_textboxes_easyocr(
            result[0][0],
            padding=int(height*0.01)
        )
        end = datetime.now()
        delta: timedelta = end - start
        print(f"Merging took {delta.total_seconds()}s for page {page_num}")
        for item in merged_regions:
            count += 1
            nums: list[int] = []
            for np_num in item:
                nums.append(int(np_num))
            region_list = [nums[0],nums[2],nums[1],nums[3]]
            box_width: int =  nums[1] - nums[0]
            box_height: int = nums[3] - nums[2]
            percent_width: int = round(box_width / width * 100)
            percent_height: int = round(box_height / height * 100)
            drawer.rectangle(region_list, outline='red')
            region = img.crop((nums[0],nums[2],nums[1],nums[3]))
            text: str = recogniser(region)
            textbox: Textbox = Textbox(
                top=round(nums[2]/height*100),
                left=round(nums[0]/width*100),
                height=int(percent_height),
                width=int(percent_width),
                text=text
            )
            textboxes.append(textbox)
            page.textboxes = textboxes
        print(f"Done with page {page_num}")
    img.save(f'outputs/test-ocr-{page_num}.png')
    print(f"Image saved to outputs/test-ocr-{page_num}.png")

final_html = make_html_file(pages)
with open("./HELP.html", "w", encoding="utf-8") as f:
    f.write(final_html)