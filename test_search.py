import asyncio
from moviebox_api.v3.http_client import MovieBoxHttpClient
from moviebox_api.v3.core import SearchV2
from moviebox_api.v1.constants import SubjectType

async def main():
    async with MovieBoxHttpClient() as client_session:
        searcher = SearchV2(
            client_session=client_session, 
            query="batman", 
            subject_type=SubjectType(0), 
            page=1, 
            per_page=30
        )
        results = await searcher.get_content()
        print(results)

if __name__ == "__main__":
    asyncio.run(main())
