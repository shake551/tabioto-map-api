from fastapi import FastAPI

from api.router import tabioto

app = FastAPI()


@app.get("/health")
async def health():
    return {"message": "ok"}


app.include_router(tabioto.router)
