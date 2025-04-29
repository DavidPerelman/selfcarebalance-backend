from fastapi import FastAPI

app = FastAPI(
    title="SelfCareBalance API",
    description="מצא את האיזון שבך | Find your inner balance",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Welcome to SelfCareBalance API!"}
