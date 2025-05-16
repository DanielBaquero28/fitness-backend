from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import users, goals, logs

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS from frontend domain
origins = [
    "http://localhost:3000", #dev
    "https://fitness-frontend-five.vercel.app" #prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(goals.router)
app.include_router(logs.router)

@app.get("/")
def root() -> dict:
    return {"message": "Fitness Tracker API is live"}