import asyncio

import httpx

ANNOUNCEMENT_URL = "https://raw.githubusercontent.com/AuroraZiling/sangonomiya.Metadata/main/announcement"


async def getAnnouncement(version, language):
    url = f"{ANNOUNCEMENT_URL}/{version}-{language}.md"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        return res.text

