from fastapi import APIRouter

# NOTE: about routes
# docs: https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=#path-operations-with-apirouter

router = APIRouter(
    prefix="/api/v1/auth"
)


@router.post("/register")
async def register_candidate():
    return {
        "route": "register candidate"
    }


@router.post("/register/company")
async def register_company():
    return {
        "route": "company"
    }


@router.post("/login")
async def register_login():
    return {
        "route": "login"
    }
