from fastapi import FastAPI
from s3 import r2Router
from models import categoryRouter
from tortoise.contrib.fastapi import register_tortoise
from decouple import config
import logging

# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("tortoise").setLevel(logging.DEBUG)


app = FastAPI()

app.include_router(r2Router, tags=['R2'])
app.include_router(categoryRouter, prefix='/category', tags=['Category API'])


@app.get("/")
async def heath():
    return {"status":"good"}


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)