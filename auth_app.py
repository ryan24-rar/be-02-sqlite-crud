
#import necessary libraries

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import Client, create_client


#Getting keys from .env file

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(supabase_url, supabase_key)

#setting up FastAPI app

app = FastAPI(title="A4 Authentication API")

security = HTTPBearer()
# Define the email and password needed for authentication

class AuthRequest(BaseModel):
    email: str
    password: str



@app.get("/")
def home():
    return {"message": "Authentication API is running"}




@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: AuthRequest):
    try:
        response = supabase.auth.sign_up(
            {
                "email": credentials.email,
                "password": credentials.password,
            }
        )

        return {
            "message": "User created successfully",
            "user_id": response.user.id if response.user else None,
        }

    except Exception as error:
        print("Signup error:", repr(error))

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
    )


@app.post("/auth/login")
def login(credentials: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": credentials.email,
                "password": credentials.password,
            }
        )

        if not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "token_type": "bearer",
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Login error:", repr(error))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

@app.get("/public/info")
def public_info():
    return {
        "message": "Anyone can access this endpoint."
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        user = supabase.auth.get_user(token)

        if not user.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return user.user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

@app.get("/protected/profile")
def protected_profile(current_user=Depends(get_current_user)):
    return {
        "message": "Protected route accessed successfully!",
        "user_id": current_user.id,
        "email": current_user.email,
    }