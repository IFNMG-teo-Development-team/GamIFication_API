from fastapi import APIRouter

router = APIRouter()


@router.get("/{id_social}")
async def read_admin(id_social: int):
    return {"id_social": id_social}
