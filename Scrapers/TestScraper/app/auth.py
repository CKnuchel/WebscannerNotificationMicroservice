from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token_with_auth_service(token: str) -> dict:
    auth_service_url = "http://fastapi-auth:8000/auth/validate-token"
    response = requests.get(auth_service_url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token_with_auth_service(token)
