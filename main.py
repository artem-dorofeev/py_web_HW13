import time
import redis.asyncio as redis
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session
from sqlalchemy import text


from src.database.db import get_db
from src.routes import contacts, auth


# from src.conf.config import settings

app = FastAPI()


@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performance'] = str(during)
    return response


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "Contacts App"}) # title - змінити
    # return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")
    

# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
#                           decode_responses=True)
#     await FastAPILimiter.init(r)

# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
# app.include_router(users.router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)