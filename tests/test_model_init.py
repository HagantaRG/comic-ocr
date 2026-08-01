import contextlib
import io
import unittest
from unittest.mock import patch

from comic_ocr_reader.functions import model_init


class ModelInitTests(unittest.TestCase):
    def test_ensure_models_initialised_prints_noop_message_when_ready(self):
        with patch.object(model_init, "models_are_initialised", return_value=True):
            with patch.object(model_init, "_download_easyocr_detector") as easyocr_factory:
                with patch.object(model_init, "_download_manga_ocr") as manga_factory:
                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        result = model_init.ensure_models_initialised()

        self.assertFalse(result)
        self.assertEqual(buffer.getvalue(), "Not required! You have already initialised.\n")
        easyocr_factory.assert_not_called()
        manga_factory.assert_not_called()

    def test_ensure_models_initialised_calls_missing_factories(self):
        with patch.object(model_init, "models_are_initialised", return_value=False):
            with patch.object(model_init, "easyocr_detector_is_initialised", return_value=False):
                with patch.object(model_init, "manga_ocr_is_initialised", return_value=False):
                    calls = []

                    def easyocr_factory():
                        calls.append("easyocr")

                    def manga_factory():
                        calls.append("manga")

                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        result = model_init.ensure_models_initialised(
                            easyocr_factory=easyocr_factory,
                            manga_factory=manga_factory,
                        )

        self.assertTrue(result)
        self.assertEqual(calls, ["easyocr", "manga"])
        self.assertEqual(buffer.getvalue(), "Initialisation complete.\n")


if __name__ == "__main__":
    unittest.main()
