import builtins
import contextlib
import io
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from comic_ocr_reader import __main__ as cli


class MainFlowTests(unittest.TestCase):
    def test_main_runs_initialisation_before_ocr_processing(self):
        folder = r"C:\fake\folder"
        output = io.StringIO()

        with patch.object(cli, "ensure_models_initialised") as init_mock:
            with patch.object(cli, "Reader") as reader_mock:
                with patch.object(cli, "MangaOcr") as manga_mock:
                    with patch.object(cli, "process_page") as process_page_mock:
                        with patch.object(cli, "make_html_file", return_value="<html></html>"):
                            with patch.object(cli, "tqdm", side_effect=lambda items: items):
                                with patch.object(cli.os.path, "isdir", return_value=True):
                                    with patch.object(cli.os, "listdir", return_value=["1.jpg"]):
                                        with patch.object(Path, "is_file", return_value=True):
                                            with patch.object(builtins, "open", mock_open()):
                                                reader_mock.return_value = object()
                                                manga_mock.return_value = object()
                                                with contextlib.redirect_stdout(output):
                                                    result = cli.main(folder)

        self.assertTrue(result)
        init_mock.assert_called_once()
        reader_mock.assert_called_once()
        manga_mock.assert_called_once()
        process_page_mock.assert_called_once()

        rendered = output.getvalue()
        self.assertIn("=== Initialisation ===", rendered)
        self.assertIn("=== OCR setup ===", rendered)
        self.assertIn("=== OCR processing ===", rendered)
        self.assertLess(rendered.index("=== Initialisation ==="), rendered.index("=== OCR setup ==="))
        self.assertLess(rendered.index("=== OCR setup ==="), rendered.index("=== OCR processing ==="))


if __name__ == "__main__":
    unittest.main()
