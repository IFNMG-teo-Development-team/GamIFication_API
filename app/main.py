from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers import users, badges, stats, login, rarity

app = FastAPI(docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(badges.router)
app.include_router(stats.router)
app.include_router(rarity.router)
