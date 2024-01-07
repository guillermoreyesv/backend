from fastapi import FastAPI
from routes.v1 import register, login
from routes.v1.belvo import user_list, user_transactions, user_group_transactions
import os

app = FastAPI(
    title="Technical test for Finvero ",
    description="By Guillermo Reyes",
    version="1.0",
    docs_url=os.getenv('DOCS_URL','/docs'), 
    redoc_url=os.getenv('REDOC_URL','/redoc')
)

version = "/v1"
app.include_router(login.router, prefix=version, tags=["login"])
app.include_router(register.router, prefix=version, tags=["register"])
app.include_router(user_list.router, prefix=version, tags=["belvo"])
app.include_router(user_transactions.router, prefix=version, tags=["belvo"])
app.include_router(user_group_transactions.router, prefix=version, tags=["belvo"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")