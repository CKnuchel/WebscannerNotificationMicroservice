from fastapi import FastAPI
from .database import engine, Base
from .api import router as api_router

Base.metadata.create_all(bind=engine)  # This creates the tables in the database
app = FastAPI()

app.include_router(api_router, prefix="/subscription")



# TODO 1: Build RabbitMQ Consumer and Fire Notification Logic
# TODO 2: Build the Dockerfile for the Notification Service
# TODO 3: Add the Notification Service to the docker-compose.yml file
# TODO 4: Test the Notification Service with the RabbitMQ Producer
