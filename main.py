from fastapi import FastAPI
from routes.v1 import register, login
import os

app = FastAPI(
    title="Technical test for Finvero ",
    description="By Guillermo Reyes",
    version="1.0",
    docs_url=os.getenv('DOCS_URL','/docs'), 
    redoc_url=os.getenv('REDOC_URL','/redoc')
)

version = "/v1"
app.include_router(register.router, prefix=version, tags=["register"])
app.include_router(login.router, prefix=version, tags=["login"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")