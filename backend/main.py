from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import samples, profile, rewrite, feedback, settings

app = FastAPI(title="Write Like Me API", version="0.1.0")

origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(samples.router, prefix=PREFIX)
app.include_router(profile.router, prefix=PREFIX)
app.include_router(rewrite.router, prefix=PREFIX)
app.include_router(feedback.router, prefix=PREFIX)
app.include_router(settings.router, prefix=PREFIX)


@app.get(f"{PREFIX}/health")
def health():
    return {"status": "ok"}
