"""Carrier wave search ingestion — DuckDuckGo + multi-engine hydration."""

import httpx


async def fetch_duckduckgo(query: str) -> dict:
    url = (
        "https://api.duckduckgo.com/"
        f"?q={httpx.URL(query)}&format=json&no_html=1&skip_disambig=1"
    )
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            r = await client.get(url)
            data = r.json()
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
        except Exception as e:
            return {
                'abstract': '',
                'source': '',
                'related': [],
                'url': '',
                'error': str(e),
            }
