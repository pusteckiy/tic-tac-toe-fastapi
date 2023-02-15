import random
import string

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError

from src.game.models import games, cells
from src.auth.models import users
from src.db.core import database


async def create_game_and_code() -> str:
    letters = string.ascii_uppercase + string.digits
    game_code = ''.join(random.choice(letters) for _ in range(10))
    query = games.insert().values(code=game_code)
    try:
        await database.execute(query)
        return game_code
    except:
        raise HTTPException(status_code=500, detail='game with this code already exist, repeat request')


async def get_game(user):
    query = games.select().where(games.c.id == user.connected_game)
    game = await database.fetch_one(query)
    if not game:
        raise HTTPException(status_code=500, detail='user have not connected to the game')
    return game


async def connect_user_to_game(game_code, user):
    query = games.select().where(games.c.code == game_code)
    game = await database.fetch_one(query)
    if not game:
        raise HTTPException(status_code=400, detail="there is no game with this code")
    query = users.update().where(users.c.id == user.id).values(connected_game=game.id)
    await database.execute(query)


async def get_game_users(game_id):
    if game_id is None:
        raise HTTPException(status_code=400, detail="user have not connected to game")
    query = users.select().where(users.c.connected_game == game_id)
    return await database.fetch_all(query)


async def insert_value_in_cell(game_id: int, username: str, x: int, y: int, z: int):
    try:
        query = cells.insert().values(game=game_id, x=x, y=y, z=z, player=username)
        await database.execute(query)
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail='someone have already made move here')


async def get_game_field(game_id: int):
    query = cells.select().where(cells.c.game == game_id).order_by(cells.c.x, cells.c.y, cells.c.z)
    return await database.fetch_all(query)


async def end_game(game_id, winner):
    query = games.update().where(games.c.id == game_id).values(end=True, winner=winner)
    await database.execute(query)
    query = users.update().where(users.c.connected_game == game_id).values(connected_game = None)
    await database.execute(query)


async def make_game_move(user, x, y, z):
    game = await get_game(user)
    if game.end:
        raise HTTPException(status_code=400, detail="game already finished")
    
    await insert_value_in_cell(
        game_id=game.id,
        username=user.username,
        x=x, y=y, z=z)  
    
    field = await get_game_field(game_id=game.id)

    if check_win(field, user.username):
        await end_game(game_id=game.id, winner=user.id)
        return {'status': 'end', 'winner': user.username}
    
    query = games.update().where(games.c.id == game.id).values(next=user.id)
    await database.execute(query)
    return {'status': 'in process', 'next': ''}


def check_win(board, username):
    for x in range(3):
        row = [space for space in board if space["x"] == x and space["player"] == username]
        if len(row) == 3:
            return True
    
    # Check columns
    for y in range(3):
        column = [space for space in board if space["y"] == y and space["player"] == username]
        if len(column) == 3:
            return True
        
    # Check diagonals
    diagonal1 = [space for space in board if space["x"] == space["y"] and space["player"] == username]
    if len(diagonal1) == 3:
        return True
    
    diagonal2 = [space for space in board if space["x"] + space["y"] == 2 and space["player"] == username]
    if len(diagonal2) == 3:
        return True
    
    # Check depth
    for z in range(3):
        depth = [space for space in board if space["z"] == z and space["player"] == username]
        if len(depth) == 3:
            return True
    
    return False
