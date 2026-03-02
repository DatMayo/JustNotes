from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200, tags=["Health"])
def health():
    return {"status": "ok"}
