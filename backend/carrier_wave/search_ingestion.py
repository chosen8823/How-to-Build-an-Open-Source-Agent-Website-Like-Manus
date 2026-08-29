"""Carrier wave search ingestion — DuckDuckGo + multi-engine hydration."""

import httpx
from urllib.parse import quote_plus


async def fetch_duckduckgo(query: str) -> dict:
    """Async variant used by the WebSocket handler."""
    url = (
        "https://api.duckduckgo.com/"
        f"?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
    )
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            r = await client.get(url)
            data = r.json()
            return _parse_ddg(data)
        except Exception as e:
            return _error_result(e)


def fetch_duckduckgo_sync(query: str) -> dict:
    """Synchronous variant used by the Flask blueprint."""
    url = (
        "https://api.duckduckgo.com/"
        f"?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
    )
    with httpx.Client(timeout=5.0) as client:
        try:
            r = client.get(url)
            data = r.json()
            return _parse_ddg(data)
        except Exception as e:
            return _error_result(e)


def _parse_ddg(data: dict) -> dict:
    return {
        'abstract': data.get('AbstractText', ''),
        'source': data.get('AbstractSource', ''),
        'related': [
            t.get('Text', '')
            for t in data.get('RelatedTopics', [])[:3]
            if isinstance(t, dict)
        ],
        'url': data.get('AbstractURL', ''),
    }


def _error_result(e: Exception) -> dict:
    return {
        'abstract': '',
        'source': '',
        'related': [],
        'url': '',
        'error': str(e),
    }
