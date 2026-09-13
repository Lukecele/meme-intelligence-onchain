"""Compatibility wrapper for up-to-1000 Birdeye first buyers per configured token."""
import asyncio
from extractors.first_buyers_extractor import FirstBuyersExtractor
async def main():
    e=FirstBuyersExtractor()
    try: print('Imported rows:', await e.run(limit=1000))
    finally: await e.close()
if __name__=='__main__': asyncio.run(main())
