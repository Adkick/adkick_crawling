import httpx

async def fetch_place_ids(query, lon, lat):
    url = "https://map.naver.com/p/api/search/allSearch"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://map.naver.com/p/search/{httpx.utils.quote(query)}?c=15.00,0,0,0,dh"
    }
    params = {
        "query": query,
        "type": "all",
        "searchCoord": f"{lon};{lat}",
        "boundary": ""
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
    return [item["id"] for item in data["result"]["place"]["list"]]