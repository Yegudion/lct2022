from fastapi import APIRouter
from routes.admin import adminRouter
from routes.user import userRouter

router = APIRouter(prefix="/api")
router.include_router(adminRouter)
router.include_router(userRouter)

@router.get("/")
async def root():
    return {"message": "Hello Api"}
