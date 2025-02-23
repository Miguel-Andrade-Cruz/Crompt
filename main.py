import requests
from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import json
from pydantic import BaseModel
from urllib.parse import urlencode

import ResponseModel



app = FastAPI()


with open("client_secret.json", "r") as f:
    creds = json.load(f)["web"]

CLIENT_ID = creds["client_id"]
REDIRECT_URI = "http://localhost:8000/auth/login/callback"



@app.post("/auth/login")
async def login():

  params = {
      "client_id": CLIENT_ID,
      "redirect_uri": REDIRECT_URI,
      "response_type": "code",
      "scope": "https://www.googleapis.com/auth/drive.file",
      "access_type": "offline",
      "prompt": "consent"
  }
  auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"

  return ResponseModel(content={"auth_url" : auth_url})



@app.get("/auth/login/callback")
async def callback(code: str):

  token_url = "https://oauth2.googleapis.com/token"

  data = {
      "code": code,
      "client_id": CLIENT_ID,
      "client_secret": creds["client_secret"],
      "redirect_uri": REDIRECT_URI,
      "grant_type": "authorization_code"
  }

  response = requests.post(token_url, data=data)
  tokens = response.json()

  if "access_token" in tokens:
      return ResponseModel(content={"access_token": tokens["access_token"], "refresh_token": tokens.get("refresh_token")})

  return ResponseModel(status_message={"error": "Failed to authenticate"})






@app.get("/search")
def info():
  pass





@app.get("/folder")
def defineFolder():

  pass