from pydantic import BaseModel
from typing import Dict, List

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

class LaserData(BaseModel):
    startX: float
    startY: float
    endX: float
    endY: float

class GameState(BaseModel):
    money: int
    lives: int
    wave: int
    enemies: Dict[str, EnemyData]
    towers: Dict[str, TowerData]
    lasers: List[LaserData]

class ActionPayload(BaseModel):
    action: str
    payload: dict