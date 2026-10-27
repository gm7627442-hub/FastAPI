import json
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from redis_client import redis_conn
import workers

app = FastAPI(title="Redis & Background Tasks API")

articles = []

class Article(BaseModel):
    id: int
    title: str
    content: str

@app.get("/articles", response_model=list[Article])
def get_articles():
    cached_data = redis_conn.get("articles_list")
    if cached_data:
        return json.loads(cached_data)
    
    redis_conn.setex("articles_list", 60, json.dumps(articles))
    return articles

@app.get("/articles/{id}", response_model=Article)
def get_article(id: int):
    cache_key = f"article:{id}"
    cached_data = redis_conn.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    target_article = None
    for art in articles:
        if art["id"] == id:
            target_article = art
            break
            
    if not target_article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    redis_conn.setex(cache_key, 60, json.dumps(target_article))
    return target_article

@app.post("/articles", response_model=Article, status_code=201)
def create_article(article: Article, background_tasks: BackgroundTasks):
    for art in articles:
        if art["id"] == article.id:
            raise HTTPException(status_code=400, detail="Article with this ID already exists")
            
    new_article = article.model_dump()
    articles.append(new_article)
    
    redis_conn.delete("articles_list")
    
    background_tasks.add_task(workers.log_article_creation, article.id)
    return new_article

@app.delete("/cache", status_code=204)
def clear_cache():
    redis_conn.delete("articles_list")
    return None
