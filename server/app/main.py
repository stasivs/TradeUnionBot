import uvicorn
from fastapi import FastAPI
from routes.student import router as StudentRouter


app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")


uvicorn.run(app, host="0.0.0.0", port=8000)