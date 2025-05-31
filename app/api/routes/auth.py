from fastapi import APIRouter, HTTPException, Depends
from app.models.auth import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.service_facade import app_facade

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    try:
        result = await app_facade.register_new_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )
        
        if not result["registered"]:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result["user_data"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    try:
        result = await app_facade.authenticate_and_get_profile(
            email=user_data.email,
            password=user_data.password
        )
        
        if not result["authenticated"]:
            raise HTTPException(status_code=401, detail=result["error"])
            
        return result["user_data"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
