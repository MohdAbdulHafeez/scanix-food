import asyncio
import httpx

async def test():
    API_KEY = "YOUR_API_KEY"  # Paste your key here temporarily
    CX_ID = "YOUR_CX_ID"      # Paste your CX ID here temporarily
    
    params = {
        "key": API_KEY,
        "cx": CX_ID,
        "q": "healthy alternatives to Lays chips",
        "num": 5
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/customsearch/v1",
            params=params
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

asyncio.run(test())