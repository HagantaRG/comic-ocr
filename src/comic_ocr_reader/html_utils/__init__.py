from pathlib import Path

HTML_UTILS_FOLDER: Path = Path(__file__).parent
class Textbox:
    """Class containing details of the textbox on a page
    Attributes:
        top     %-age of page down from top of page to place textbox.
        left    %-age of page right from left of page to place textbox.
        width   %-age width of textbox in terms of containing page.
        height  %-age height of textbox in terms of containing page.
    """
    top: int
    left: int
    width: int
    height: int
    text: str
    btn_class: str
    def __init__(
            self,
            top: int,
            left: int,
            width: int,
            height: int,
            text: str
    ) -> None:
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.text = text

class Page:
    textboxes: list[Textbox] = []
    img_filepath: Path
    page_num: int
    page_html: str
    page_class: str

    def __init__(
            self,
            img_filepath: Path|str,
            page_num: int,
            page_class: str
    ):
        self.img_filepath = img_filepath
        self.page_num = page_num
        self.page_class = page_class

    def make_page_html(self) -> None:
        """
        Constructs the HTML of a page, shoves it into the page_html attribute of this object.
        :return:
        """
        page_html: str = f"""
        <div class="{self.page_class}" id="page{self.page_num}">
        <button class="page-nav prev" onclick="lastPage()">Prev. Page</button>
        <button class="page-nav next" onclick="nextPage()">Next Page</button>
        <div class="zoom-hint">Ctrl + wheel to zoom</div>
        <div class="page-content">
        <div class="page-content-inner">
        <img src="{self.img_filepath}" alt="Snow">
        """
        for textbox in self.textboxes:
            page_html += f"""
            <button class="text-btn"
                    style="--top:{textbox.top}%;--left:{textbox.left}%;--height:{textbox.height}%;--width:{textbox.width}%;">
                <span>{textbox.text}</span>
            </button>
            """
        page_html+="""
        </div>
        </div>
        </div>
        """
        self.page_html = page_html

    def set_page_class(self, page_class: str):
        self.page_class = page_class


def make_html_file(
        pages: dict[int, Page],
        template: str|Path = f"{HTML_UTILS_FOLDER}/html_template.html"
) -> str:
    html_body: str = ""
    for i in range(1, len(pages.keys())+1):
        if (i - 1) % 2 == 0:
            html_body += """
            <div class="spread">
            <button class="spread-nav prev" onclick="lastPage()">Prev. Page</button>
            <button class="spread-nav next" onclick="nextPage()">Next Page</button>
            <div class="spread-hint">Ctrl + wheel to zoom</div>
            <div class="spread-scroll">
            <div class="spread-content">
            """
        if i == len(pages):
            pages[i].set_page_class("page last")
        elif i == 1:
            pages[i].set_page_class("page first")
        pages[i].make_page_html()
        html_body += pages[i].page_html
        if (i - 1) % 2 == 1 or i == len(pages):
            html_body += """
            </div>
            </div>
            </div>
            """
    with open(template, "r", encoding="utf-8") as html_template:
        template: str = html_template.read()
        template = template.replace("{{BODY}}", html_body)
    return template
