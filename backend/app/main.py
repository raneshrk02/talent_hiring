from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .mongodb import get_mongo_db
from .routes import chat, export

 # MongoDB does not require table creation

app = FastAPI(title="TalentScout API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(export.router, prefix="/api", tags=["export"])

@app.get("/")
async def root():
    return {"message": "TalentScout API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}