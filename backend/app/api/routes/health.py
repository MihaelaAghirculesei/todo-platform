from fastapi import APIRouter

router = APIRouter()


# HEAD is accepted too: uptime monitors check availability with HEAD requests.
@router.api_route("/health", methods=["GET", "HEAD"])
def health_check() -> dict:
    return {"status": "ok"}
