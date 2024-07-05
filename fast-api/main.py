from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/vtv_news_db_prod")
db = client["vtv_news_db_prod"]
collection = db["thegioi_news"]

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/news/", response_class=JSONResponse)
async def get_news(
    keyword: str = Query("", description="Filter by title keyword"),
    page: int = 1,
    size: int = 10,
    sort: str = "scraped_time",
    order: str = "desc",
):
    filter_query = {}
    if keyword:
        filter_query = {"title": {"$regex": keyword, "$options": "i"}}

    cursor = collection.find(filter_query)
    cursor = cursor.sort([(sort, -1) if order == "desc" else (sort, 1)])
    total = collection.count_documents(filter_query)
    items = list(cursor.skip((page - 1) * size).limit(size))
    return {
        "total": total,
        "items": serialize_news(items),
        "page": page,
        "size": size,
    }

@app.get("/api/v1/news/{news_id}", response_class=JSONResponse)
async def get_news_detail(news_id: str):
    news = collection.find_one({"original_id": news_id})
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    news["_id"] = str(news["_id"])  # Convert ObjectId to string
    return news

def serialize_new(new):
    new["id"] = str(new["_id"])
    new.pop("_id")
    return new

def serialize_news(news):
    return [serialize_new(new) for new in news]