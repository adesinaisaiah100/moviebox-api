from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from moviebox_api.v3.http_client import MovieBoxHttpClient
from moviebox_api.v3.core import SearchV2, ItemDetails, DownloadableVideoFilesDetail
from moviebox_api.v1.constants import SubjectType

app = FastAPI(
    title="Moviebox API",
    description="Web wrapper for moviebox-api repository to be used in React App",
    version="1.0.0"
)

# Allow your React app to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust this to your specific React app domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Moviebox API is running!"}

@app.get("/search")
async def search_contents(
    query: str = Query(..., description="The query string to search for"),
    subject_type: int = Query(0, description="0=All, 1=Movies, 2=TV Series"),
    page: int = Query(1, description="Page number for pagination"),
    per_page: int = Query(30, description="Items per page")
):
    try:
        s_type = SubjectType(subject_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid subject_type. Must be 0, 1, or 2.")
        
    async with MovieBoxHttpClient() as client_session:
        searcher = SearchV2(
            client_session=client_session, 
            query=query, 
            subject_type=s_type, 
            page=page, 
            per_page=per_page
        )
        try:
            results = await searcher.get_content()
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/details/{item_id}")
async def get_item_details(item_id: str):
    async with MovieBoxHttpClient() as client_session:
        details = ItemDetails(client_session)
        try:
            result = await details.get_content(item_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{item_id}")
async def get_download_links(item_id: str):
    async with MovieBoxHttpClient() as client_session:
        downloader = DownloadableVideoFilesDetail(client_session)
        try:
            result = await downloader.get_content(item_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
