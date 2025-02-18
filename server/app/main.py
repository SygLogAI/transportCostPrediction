from fastapi import FastAPI
from routers import transport_cost
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transport_cost.router, prefix="/api/models")

@app.get("/api")
async def root():
    return {"message": "Sygnus AI model service"}
