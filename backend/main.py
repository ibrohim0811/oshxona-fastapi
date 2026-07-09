from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.api.category import router as category
from backend.api.item import router as item
from backend.api.order import router as order
from backend.api.user import router as user



app = FastAPI()

# CORS — frontend (auth.html / home.html) brauzerdan API ga murojaat qila olishi uchun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ishlab chiqishda hammasi ochiq; prod'da domenlarni yozing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category)
app.include_router(item)
app.include_router(order)
app.include_router(user)

@app.get('/root/')
async def root():
    return {"message":"ok"}