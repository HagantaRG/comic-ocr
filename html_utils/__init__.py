from pathlib import Path

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
    textboxes: list[Textbox]
    img_filepath: Path
    page_num: int
    buttons_css: str
    page_html: str

    def __init__(
            self,
            img_filepath: Path,
            page_num: int
    ):
        self.img_filepath = img_filepath
        self.page_num = page_num

    def make_textboxes_css(
            self
    ) -> None:
        """
        Constructs the CSS required to style buttons on this page. Shoves that into the
        buttons_css atttribute of this object.
        :return:
        """
        button_css: str = ""
        count: int = 0
        for textbox in self.textboxes:
            count += 1
            button_css += f"""
                    .container .btn-page{self.page_num}-{count} {{
                      position: absolute;
                      top: {textbox.top}%;
                      left: {textbox.left}%;
                      width: {textbox.width}%;
                      height: {textbox.height}%;
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
                    .container .btn-page{self.page_num}-{count}:hover {{
                      background-color: black;
                      opacity: 100;
                    }}
                    """
            textbox.btn_class = f"btn-page{self.page_num}-{count}"
        self.buttons_css = button_css

    def make_page_html(self) -> None:
        """
        Constructs the HTML of a page, shoves it into the page_html attribute of this object.
        :return:
        """
        page_html: str = f"""
        <div class="container" id="page-{self.page_num}">
        <img src="{self.img_filepath}" alt="Snow">
        """
        for textbox in self.textboxes:
            page_html += f"""
            <button class="{textbox.btn_class}">{textbox.text}</button>
            """
        self.page_html = page_html


def make_html_file() -> str:
    ...
