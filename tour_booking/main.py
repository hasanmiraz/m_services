from fastapi import APIRouter

app2_router = APIRouter()

@app2_router.get("/")
def read_app2():
    return {"message": "This is app2"}
