from fastapi import FastAPI 
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from database import init_db, close_db
from users_handler import *
from portfolio_handler import *
from middleware import *
from tokens import *
from llm import *

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server started successfully")
    await init_db()
    yield
    await close_db()
    print("Server shut down successfully")

app=FastAPI(lifespan=lifespan)



@app.get("/health")
def check_health():
    return {"server up and running"}

@app.post("/signup")
def signup():
    response=signup_handler()
    return response

@app.post("/login")
def login():
    response=login_handler()
    return response

@app.get("/renew_access_token")
def renew_access_token():
    response=renew_access_token_handler()
    return response

@app.post("/create_portfolio")
def create_portfolio():
    response=portfolio_creation_handler() #the handler does everything from text extraction from pdf to calling llm, creating the exact portfolio document in db
    return response 

@app.post("/submit_edits")
def submit_edits():
    response=portfolio_edits_handler() #this handler would fill remaining details which could not be extracted from resume and saves to db
    return response


@app.post("/check_llm")
def check_llm():
    response=extract_info_from_resume()
    return response



