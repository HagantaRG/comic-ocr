from PIL import Image, ImageDraw, ImageText, ImageFont
from easyocr import Reader
from manga_ocr import MangaOcr

from html_utils import Textbox
detector = Reader(
    lang_list=['ja'],
    recognizer=False
)
file: str = "test-pics/test-ocr-2.png"
result = detector.detect(file)
recogniser = MangaOcr()
region_count: int = 0
html_styles: str = ""
html_buttons: str = ""
final_html: str = ""
with Image.open('test-pics/test-ocr-2.png') as img:
    width, height = img.size
    drawer = ImageDraw.Draw(img)
    count: int = 0
    print(f"Image is {width}x{height}")
    for item in result[0][0]:
        count += 1
        nums: list[float] = []
        for np_num in item:
            nums.append(float(np_num))
        region_list = [nums[0],nums[2],nums[1],nums[3]]
        print(f"""Box has coords:
        xmin: {nums[0]}px
        xmax: {nums[1]}px
        ymin: {nums[2]}px
        ymax: {nums[3]}px
        """)
        box_width: float =  nums[1] - nums[0]
        box_height: float = nums[3] - nums[2]
        print(f"Box is {box_width}x{box_height}")
        percent_width: int = int(box_width / width * 100)
        percent_height: int = int(box_height / height * 100)
        print(f"Box is {percent_width}%x{percent_height}%")
        drawer.rectangle(region_list, outline='red')
        region = img.crop((nums[0],nums[2],nums[1],nums[3]))
        text: str = recogniser(region)
        print(text)
        html_styles += f"""
        .container .btn{count} {{
          position: absolute;
          top: {int(nums[2]/height*100)}%;
          left: {int(nums[0]/width*100)}%;
          width: {percent_width}%;
          height: {percent_height}%;
          background: rgba(0,0,0,0.1);
          color: white;
          font-size: 2cqw;
          padding: 12px 24px;
          border: none;
          cursor: pointer;
          border-radius: 5px;
          writing-mode: vertical-rl;
          text-orientation: upright;
          opacity: 0;
        }}
        .container .btn{count}:hover {{
          background-color: black;
          opacity: 100;
        }}
        """
        html_buttons += f"""
        <button class="btn{count}">{text}</button>
        """
    img.save('outputs/test-ocr-2.png')
    final_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <meta charset="UTF-8">
        <style>
            /* Container needed to position the button. Adjust the width as needed */
        .container {{
          position: relative;
          width: 75%;
          container-type: inline-size;
        }}
        
        /* Make the image responsive */
        .container img {{
          width: 100%;
          height: auto;
        }}
        
        {html_styles}
        
        </style>
        <body>
        <div class="container">
        <img src="{file}" alt="Snow">
            {html_buttons}
        </div>
        </body>
        </html>
    """
with open("HELP.html", "w", encoding="utf-8") as f:
    f.write(final_html)