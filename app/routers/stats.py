from fastapi import APIRouter


router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_stats():
    #create_user_badges()
    return [{"id": 1,
             "id_medal": 1,
             "data_aquired": "30/11/2022",
             "soft_delete": None},
            {"id": 2,
             "id_medal": 1,
             "data_aquired": "30/11/2022",
             "soft_delete": None
             }
            ]
