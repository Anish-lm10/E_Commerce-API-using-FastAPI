from fastapi import FastAPI
from auth_routes import *
from order_routes import *


app = FastAPI()


app.include_router(auth_router)
app.include_router(order_router)


@app.get("/")
async def hello():
    """
    ## Main Route
    """
    return {"message": "hello main"}
