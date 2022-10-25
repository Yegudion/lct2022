import logging

from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles

from .sql_app import models
from .sql_app.database import engine
from .priceByCityDistrict import Parser
from .routes.index import router

logging.basicConfig(format="%(asctime)s [%(name)s] - %(levelname)s: %(message)s", level=logging.INFO)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/web", StaticFiles(directory=''), name="static")

logger = logging.getLogger(__name__)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "ok"}

parser = Parser()
parser.start()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
