from fastapi import FastAPI

app = FastAPI(title="Atlas Reliability Framework", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}