from fastapi import FastAPI
from api.routes.search import router as search_router

app = FastAPI(title="IT Services Resolution API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(search_router, prefix="/search", tags=["search"])


@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "service": "itservices-resolution-api"
    }
