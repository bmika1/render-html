import webbrowser
import tempfile

from src.html_renderer.exceptions import BrowserNotFoundException, UnknownBrowserException


def _open_in_browser(file_path: str, browser: str | None = None) -> None:
    """
    Open the specified file path in a web browser.

    Args:
        file_path (str): The path of the file to open.
        browser (str | None, optional): The web browser to use (i.e. "chrome", "safari").
            If provided, the HTML content will be opened using the specified browser.
            If not provided or set to None, the default browser will be used.
    """
    if browser:
        try:
            client = webbrowser.get(browser)
        except webbrowser.Error as e:
            if "could not locate runnable browser" in str(e):
                raise BrowserNotFoundException(browser)
            raise UnknownBrowserException(e)
    else:
        client = webbrowser
    if not file_path.startswith("file://"):
        file_path = f"file://{file_path}"
    client.open_new(file_path)


def _handle_open_from_temp(html_string: str, browser: str | None = None) -> None:
    """
    Handle opening HTML content from a temporary file in a web browser.

    Args:
        html_string (str): The HTML content as a string.
        browser (str | None, optional): The web browser to use (i.e. "chrome", "safari").
            If provided, the HTML content will be opened using the specified browser.
            If not provided or set to None, the default browser will be used.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=True, suffix='.html') as tmp_file:
        tmp_file.write(html_string)
        file_path = tmp_file.name
        _open_in_browser(file_path, browser)
        tmp_file.close()


def _handle_open_from_regular_file(html_string: str, save_path: str, browser: str | None = None) -> None:
    """
    Handle opening HTML content from a regular file in a web browser.

    Args:
        html_string (str): The HTML content as a string.
        save_path (str): The path to save the HTML content as a file.
        browser (str | None, optional): The executable path of the web browser to use.
            If provided, the HTML content will be opened using the specified browser.
            If not provided or set to None, the default browser will be used.
    """
    with open(save_path, 'w') as f:
        f.write(html_string)
    _open_in_browser(save_path, browser)


def render_in_browser(html_string: str, save_path: str | None = None, browser: str | None = None) -> None:
    """
    Render the HTML content in a web browser.

    Args:
        html_string (str): The HTML content as a string.
        save_path (str | None, optional): The path to save the HTML content as a file.
            If provided, the HTML content will be saved to the specified file
            and opened from it. If not provided or set to None, a temporary file
            will be created in the operating system's default temporary directory.
            The temporary file will be removed once the rendering is complete.
            IMPORTANT: Please provide an absolute path to your file.
        browser (str | None, optional): The web browser to use (i.e. "chrome", "safari").
            If provided, the HTML content will be opened using the specified browser.
            If not provided or set to None, the default browser will be used.
    """
    if save_path:
        _handle_open_from_regular_file(html_string, save_path, browser)
    else:
        _handle_open_from_temp(html_string, browser)
