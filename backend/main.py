from fastapi import FastAPI


from backend.api.category import router as category
from backend.api.item import router as item
from backend.api.order import router as order
from backend.api.user import router as user



app = FastAPI()
app.include_router(category)
app.include_router(item)
app.include_router(order)
app.include_router(user)

@app.get('/root/')
async def root():
    return {"message":"ok"}