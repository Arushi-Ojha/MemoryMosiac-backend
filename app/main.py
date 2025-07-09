from fastapi import FastAPI, Depends
from app.database import verify_connection, SessionLocal , engine
from sqlalchemy.orm import Session
from app import models, schemas, auth, upload
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(upload.router)

@app.on_event("startup")
def startup_event():
    verify_connection()

@app.get("/")
def read_root():
    return {"message": "Welcome to MemoryMosaic API!"}
