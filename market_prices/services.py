
import time
import requests

from django.conf import settings


AGMARKNET_API_URL = (
    'https://api.data.gov.in/resource/'
    '9ef84268-d588-465a-a308-a864a43d0070'
)


class AgmarknetAPIError(Exception):
    """Raised when the Agmarknet API request or response fails."""
    pass


def fetch_market_prices(limit=10, offset=0):
    """
    Fetch market-price records from the official data.gov.in API.
    """

    api_key = settings.AGMARKNET_API_KEY

    if not api_key:
        raise AgmarknetAPIError(
            'Agmarknet API key is missing. Check your .env file.'
        )

    if limit < 1 or offset < 0:
        raise ValueError(
            'Limit must be positive and offset cannot be negative.'
        )

    params = {
        'api-key': api_key,
        'format': 'json',
        'limit': limit,
        'offset': offset,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = None

    for attempt in range(3):

        try:
            response = requests.get(
                AGMARKNET_API_URL,
                params=params,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            break

        except requests.exceptions.Timeout as exc:

            if attempt == 2:
                raise AgmarknetAPIError(
                    'Agmarknet API timed out after three attempts.'
                ) from exc

            time.sleep(2 ** attempt)

        except requests.exceptions.ConnectionError as exc:

            if attempt == 2:
                raise AgmarknetAPIError(
                    'Could not connect to Agmarknet after three attempts.'
                ) from exc

            time.sleep(2 ** attempt)

        except requests.exceptions.HTTPError as exc:
            raise AgmarknetAPIError(
                f'Agmarknet API returned HTTP {response.status_code}.'
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise AgmarknetAPIError(
                f'Agmarknet request failed: {exc}'
            ) from exc

    try:
        data = response.json()

    except ValueError as exc:
        raise AgmarknetAPIError(
            'Agmarknet returned an invalid JSON response.'
        ) from exc

    if not isinstance(data, dict):
        raise AgmarknetAPIError(
            'Unexpected API response format.'
        )

    if data.get('status') != 'ok':
        raise AgmarknetAPIError(
            data.get('error')
            or data.get('message')
            or 'Agmarknet API reported an unsuccessful response.'
        )

    records = data.get('records')

    if not isinstance(records, list):
        raise AgmarknetAPIError(
            'API response does not contain a valid records list.'
        )

    return records
