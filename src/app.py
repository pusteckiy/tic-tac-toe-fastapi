from fastapi import FastAPI, APIRouter

from src.db.core import database, engine, metadata
from src.auth.router import router as auth_router
from src.game.router import router as game_router


metadata.create_all(bind=engine)


app = FastAPI(
    title='TicTacToeAPI',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router)
app.include_router(game_router)
