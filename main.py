from fastapi import FastAPI
from models import Base
from database import engine
from routers import mushrooms, baskets

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Грибы и корзинки API")

app.include_router(mushrooms.router, prefix="/mushrooms", tags=["mushrooms"])
app.include_router(baskets.router, prefix="/baskets", tags=["baskets"])

@app.get("/")
async def root():
    return {"message": "API грибов и корзинок!"}
