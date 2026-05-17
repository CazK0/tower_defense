from pydantic import BaseModel
from typing import Dict

class Position(BaseModel):
    x: float
    y: float

class EnemyData(BaseModel):
    id: str
    type: str
    hp: int
    speed: float
    pos: Position

class TowerData(BaseModel):
    id: str
    type: str
    damage: int
    radius: float
    pos: Position

class GameState(BaseModel):
    money: int
    lives: int
    wave: int
    enemies: Dict[str, EnemyData]
    towers: Dict[str, TowerData]

class ActionPayload(BaseModel):
    action: str
    payload: dict