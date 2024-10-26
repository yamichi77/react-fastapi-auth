from api.router import auth, response

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:5173",  # ReactアプリのURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Authorizationヘッダーを許可するために設定
)

app.include_router(auth.router)
app.include_router(response.router)
