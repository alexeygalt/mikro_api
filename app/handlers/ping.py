from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=['ping'])

router.get('/')


@router.get('/app')
async def ping_ap():
    return {"text": "app is working"}


@router.get('/db')
async def ping_ap():
    return {"message": "ok"}