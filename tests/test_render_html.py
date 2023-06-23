import unittest
from unittest.mock import patch, MagicMock

from src.render_html.exceptions import BrowserNotFoundException
from src.render_html._renderer import (
    render_in_browser,
    _handle_open_from_regular_file,
    _handle_open_from_temp,
)


class RendererTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_string = "<html><body><h1>Hello, World!</h1></body></html>"
        cls.save_path = "/path/to/save/file.html"
        cls.temp_path = "/path/to/temp/file.html"

    def test_handle_open_from_regular_file(self):
        with patch("builtins.open", create=True) as mock_open, patch(
            "webbrowser.open_new"
        ) as mock_webbrowser_open:
            mock_file = MagicMock()
            mock_file.name = self.save_path
            mock_open.return_value.__enter__.return_value = mock_file
            _handle_open_from_regular_file(self.html_string, self.save_path)
            mock_open.assert_called_once_with(self.save_path, "w")
            mock_file.write.assert_called_once_with(self.html_string)
            mock_webbrowser_open.assert_called_once_with(f"file:///{mock_file.name}")

    def test_handle_open_from_temp(self):
        with patch("tempfile.NamedTemporaryFile", create=True) as mock_tempfile, patch(
            "webbrowser.open_new"
        ) as mock_webbrowser_open:
            mock_file = MagicMock()
            mock_tempfile.return_value.__enter__.return_value = mock_file
            mock_file.name = self.temp_path
            _handle_open_from_temp(self.html_string)
            mock_tempfile.assert_called_once_with(mode="w", delete=True, suffix=".html")
            mock_file.write.assert_called_once_with(self.html_string)
            mock_webbrowser_open.assert_called_once_with(f"file:///{mock_file.name}")

    def test_render_in_browser_save_path(self):
        with patch("builtins.open", create=True) as mock_open, patch(
            "webbrowser.open_new"
        ) as mock_webbrowser_open:
            mock_file = MagicMock()
            mock_file.name = self.save_path
            mock_open.return_value.__enter__.return_value = mock_file
            render_in_browser(self.html_string, save_path=self.save_path)
            mock_open.assert_called_once_with(self.save_path, "w")
            mock_file.write.assert_called_once_with(self.html_string)
            mock_webbrowser_open.assert_called_once_with(f"file:///{mock_file.name}")

    def test_render_in_browser_temp_file(self):
        with patch("tempfile.NamedTemporaryFile", create=True) as mock_tempfile, patch(
            "webbrowser.open_new"
        ) as mock_webbrowser_open:
            mock_file = MagicMock()
            mock_tempfile.return_value.__enter__.return_value = mock_file
            mock_file.name = self.temp_path
            render_in_browser(self.html_string)
            mock_tempfile.assert_called_once_with(mode="w", delete=True, suffix=".html")
            mock_file.write.assert_called_once_with(self.html_string)
            mock_webbrowser_open.assert_called_once_with(f"file:///{mock_file.name}")

    def test_render_in_browser_browser_not_found(self):
        with patch("tempfile.NamedTemporaryFile", create=False):
            with self.assertRaises(BrowserNotFoundException):
                render_in_browser(self.html_string, browser="invalid_browser")


if __name__ == "__main__":
    unittest.main()
