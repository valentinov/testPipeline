import time
import logging
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

# Optional: configure basic logging if not done elsewhere
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def make_request(
    method,
    url,
    *,
    headers=None,
    json=None,
    max_retries=3,
    timeout=10,
    backoff_factor=2
):
    """
    Makes a robust HTTP request with retries, timeout, and error handling.

    Parameters:
    - method: HTTP method ('GET', 'POST', etc.)
    - url: Target URL
    - headers: Optional headers for the request
    - json: Optional JSON payload (for POST/PUT)
    - max_retries: How many times to retry on failure
    - timeout: Seconds to wait for response before timing out
    - backoff_factor: Exponential backoff factor between retries

    Returns:
    - requests.Response object if successful

    Raises:
    - RuntimeError with clear message if all retry attempts fail
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Make the HTTP request with timeout
            response = requests.request(
                method,
                url,
                headers=headers,
                json=json,
                timeout=timeout
            )

            # Raise HTTPError for bad status codes (4xx, 5xx)
            response.raise_for_status()

            return response  # Success — return response object

        except (HTTPError, Timeout, RequestException) as e:
            # Final attempt: raise a cleaner RuntimeError
            if attempt == max_retries:
                error_type = type(e).__name__
                message = (
                    f"[HTTP {method}] Request to {url} failed after {max_retries} attempts.\n"
                    f"Error Type: {error_type}\n"
                    f"Error Message: {str(e)}"
                )
                raise RuntimeError(message) from e

            # Intermediate attempt: log warning and backoff
            wait = backoff_factor ** (attempt - 1)
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

if __name__ == "__main__":
    response = make_request("GET", "https://example.com/api")
    print(response.json())