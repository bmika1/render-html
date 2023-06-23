class BrowserNotFoundException(Exception):
    def __init__(self, browser: str):
        super(BrowserNotFoundException, self).__init__(f"Browser not found: {browser}")


class UnknownBrowserException(Exception):
    def __init__(self, e: Exception):
        super(UnknownBrowserException, self).__init__(
            f"Unknown webbrowser exception: {str(e)}"
        )
