from fastapi import APIRouter, Depends

from src.auth.schemas import User
from src.auth.services import get_user_by_token
from src.game import services
from src.game.schemas import Coordinate, CoordWithPlayer



router = APIRouter(
    prefix='/game',
    tags=['Game']
)


@router.post('/create')
async def create_game_and_code(user: str = Depends(get_user_by_token)):
    """ Creates a new game and returns a unique code for the game.
    """
    game_code = await services.create_game_and_code()
    await services.connect_user_to_game(game_code, user)
    return {'code': game_code, 'detail': 'game succesfully created'}


@router.put('/connect/{game_code}')
async def connect_user_to_game(game_code: str, user: str = Depends(get_user_by_token)):
    """ Connects a user to a game based on the game code.
    """
    await services.connect_user_to_game(game_code, user)
    return {'detail': f'connected to the game {game_code}'}


@router.get('/players')
async def get_game_users(user: str = Depends(get_user_by_token)) -> list[User]:
    """ Return list of users that connected to current game.
    """
    return await services.get_game_users(user.connected_game)


@router.post('/move')
async def make_game_move(coord: Coordinate, user: str = Depends(get_user_by_token)):
    """ Takes the coordinates and makes a move on the field.
    """
    return await services.make_game_move(user, coord.x, coord.y, coord.z)


@router.get('/field')
async def get_game_field(user: str = Depends(get_user_by_token)) -> list[CoordWithPlayer]:
    """ Returns the field of the game.
    """
    return await services.get_game_field(user.connected_game)