from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schema import User
from app.models.pydantic_models import LoginRequest, TokenResponse, UserResponse
from app.core.auth import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates system users (Clinicians and Admins) and returns a signed JWT access token.
    """
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
        
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "user_id": user.user_id}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.user_id,
        username=user.username,
        role=user.role,
        full_name=user.full_name
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns profile and role permissions for the currently authenticated user.
    """
    return current_user
