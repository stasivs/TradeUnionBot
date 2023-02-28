import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import Response
from routes.student import router as StudentRouter
from routes.timetable import router as TimetableRouter
from cryptography.fernet import Fernet
from os import environ

COMMON_KEY = environ.get('COMMON_KEY')

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")

app.include_router(TimetableRouter, tags=['Timetable'], prefix="/timetable")


@app.middleware("http")
async def data_encryption(request: Request, call_next):
    response = await call_next(request)
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk 
    common_key = Fernet(COMMON_KEY)  # Here is COMMON_KEY
    secret_response_body = common_key.encrypt(response_body)    
    print(f"response_body={secret_response_body.decode()}")
    return Response(content=secret_response_body, 
                    status_code=response.status_code)


uvicorn.run(app, host="0.0.0.0", port=8000)
