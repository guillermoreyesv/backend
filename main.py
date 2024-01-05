from fastapi import FastAPI
import os

app = FastAPI(
    title="Technical test for Finvero ",
    description="By Guillermo Reyes",
    version="1.0",
    docs_url=os.getenv('DOCS_URL','/docs'), 
    redoc_url=os.getenv('REDOC_URL','/redoc')
)

version = "/v1"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")