
import requests

from poll_analyzer.config import WAHLRECHT_URL


def fetch_html(url: str = WAHLRECHT_URL) -> str:
    """
    Fetch HTML from the given URL. Returns the raw HTML as a string.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text