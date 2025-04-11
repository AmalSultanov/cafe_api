from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/register')
async def registration():
    pass


@auth_router.post('/login')
async def login():
    pass


@auth_router.get('/logout')
async def logout():
    pass
