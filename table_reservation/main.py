from fastapi import APIRouter

app3_router = APIRouter()

@app3_router.get("/")
def read_app3():
    return {"message": "This is app3"}