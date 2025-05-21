import requests

class WebsiteFetcher:
    def __init__(self, url: str):
        self.url = url
        self.content = ""

    def fetch(self) -> str:
        """
        Fetches the content of the website and stores it in the instance.
        
        Returns:
            str: The raw HTML/text content of the website.

        Raises:
            requests.RequestException: If the request fails.
        """
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        self.content = response.text
        return self.content

    def get_content(self) -> str:
        """
        Returns the last fetched content.

        Returns:
            str: Previously fetched website content, or empty string.
        """
        return self.content
