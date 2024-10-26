import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()


def token_check(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = cred.credentials
    response = requests.get(
        "http://fastapi:8000/token", headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="トークンが無効です")
    return


@router.get("/response")
def response(_=Depends(token_check)):
    return {"message": "Hello, World!"}
