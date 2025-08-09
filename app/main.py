from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth
from app.core.database import Base, engine
from app import models  # Import models so SQLAlchemy sees them
import os

app = FastAPI(title="Theraneusis Platform API")

# Create tables automatically at startup (skip Alembic)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)

# Allowed origins — replace with your actual frontend domains
origins = [
    "https://theraneusis.com",   # Production frontend
    "http://localhost:3000",       # Local development
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Frontends allowed to call the API
    allow_credentials=True,         # Needed if using cookies/session auth
    allow_methods=["*"],             # Allow all HTTP methods
    allow_headers=["*"],             # Allow all headers
)

@app.get("/")
def root():
    return {"message": "Theraneusis API is running!"}