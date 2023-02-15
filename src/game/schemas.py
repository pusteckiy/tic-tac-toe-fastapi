from pydantic import BaseModel, validator


class Coordinate(BaseModel):
    x: int
    y: int
    z: int

    @validator('x', 'y', 'z')
    def x_y_z_validator(cls, v):
        if not 1 <= v <= 3:
            raise ValueError(f"{v} is not in the range [1, 3]")
        return v


class CoordWithPlayer(Coordinate):
    player: str
