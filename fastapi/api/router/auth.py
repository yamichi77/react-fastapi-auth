import hashlib
import json
import os
import urllib.parse as parse

import jwt
import requests

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()

APP_BASE_URL = "http://localhost"
APP_CLIENT_ID = os.getenv("KC_CLIENT_ID")
APP_REALM_NAME = os.getenv("KC_REALM_NAME")
CLIENT_SECRET = os.getenv("KC_CLIENT_SECRET")
APP_DOCKER_URL = "http://keycloak:8080"

APP_REDIRECT_URI = "http://localhost/api/callback"

AUTH_BASE_URL = f"{APP_BASE_URL}/realms/{APP_REALM_NAME}/protocol/openid-connect/auth"

TOKEN_URL = f"{APP_DOCKER_URL}/realms/{APP_REALM_NAME}/protocol/openid-connect/token"

VALID_TOKEN_URL = (
    f"{APP_DOCKER_URL}/realms/{APP_REALM_NAME}/protocol/openid-connect/token/introspect"
)


# Keycloak Authorization Endpointへのリダイレクト
@router.get("/login")
async def login(request: Request) -> RedirectResponse:
    # ステート生成
    state = hashlib.sha256(os.urandom(32)).hexdigest()
    # Authorization Endpointへリダイレクト
    AUTH_URL = AUTH_BASE_URL + "?{}".format(  # type: ignore
        parse.urlencode(
            {
                "client_id": APP_CLIENT_ID,
                "redirect_uri": APP_REDIRECT_URI,
                "state": state,
                "response_type": "code",
                "client_secret": CLIENT_SECRET,
            }
        )
    )
    response = RedirectResponse(AUTH_URL)
    # ステート保存
    response.set_cookie(key="AUTH_STATE", value=state)
    response.set_cookie(key="REDIRECT_URL", value=request.headers["referer"])
    return response


# Token Request
def get_token(code):

    params = {
        "client_id": APP_CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": APP_REDIRECT_URI,
        "code": code,
        "client_secret": CLIENT_SECRET,
    }
    x = requests.post(TOKEN_URL, params, verify=False).content.decode("utf-8")
    data = json.loads(x)
    return data


# Redirection Endpoint
# ステートと認可コードを受け取る。
# ステート検証後、トークンリクエストを実行する。
@router.get("/callback")
async def auth(request: Request, code: str, state: str) -> RedirectResponse:
    # State検証
    if state != request.cookies.get("AUTH_STATE"):
        raise HTTPException(status_code=400, detail="state_verification_failed")
    redirect_url = request.cookies.get("REDIRECT_URL")
    redirect_url = redirect_url if redirect_url is not None else "/"
    response = RedirectResponse(redirect_url)
    data = get_token(code)
    response.set_cookie(key="AUTH_TOKEN", value=data["access_token"])
    response.set_cookie(key="AUTH_REF_TOKEN", value=data["refresh_token"])
    response.delete_cookie("AUTH_STATE")
    response.delete_cookie("REDIRECT_URL")
    return response


@router.get("/token")
async def valid_token(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = cred.credentials
    params = {
        "client_id": APP_CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "token": token,
    }
    x = requests.post(VALID_TOKEN_URL, params, verify=False).content.decode("utf-8")
    data = json.loads(x)
    if not data["active"]:
        raise HTTPException(status_code=401, detail="トークンが無効です")
    return data


@router.get("/token/refresh")
async def refresh_token(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = cred.credentials
    params = {
        "client_id": APP_CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": token,
        "grant_type": "refresh_token",
    }
    x = requests.post(TOKEN_URL, params, verify=False).content.decode("utf-8")
    data = json.loads(x)
    response = Response()
    response.set_cookie(key="AUTH_TOKEN", value=data["access_token"])
    response.set_cookie(key="AUTH_REF_TOKEN", value=data["refresh_token"])
    return response


@router.get("/token/local")
async def local_valid_token(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = cred.credentials
    return jwt.decode(token, options={"verify_signature": False})
