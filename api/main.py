from fastapi import FastAPI

from api.router import tabioto, user

app = FastAPI()


@app.get("/health")
async def health():
    return {"message": "ok"}


app.include_router(user.router)
app.include_router(tabioto.router)
