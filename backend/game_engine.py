import asyncio
import uuid
from models import GameState, EnemyData, TowerData, Position

class GameEngine:
    def __init__(self):
        self.state = GameState(
            money = 100,
            lives = 20,
            wave = 1,
            enemies = {},
            towers = {}
        )
        self.tick_rate = 1 / 30

    def process_input(self, data: dict):
        action = data.get("action")
        payload = data.get("payload", {})

        if action == "place_tower":
            tower_id = str(uuid.uuid4())
            self.state.towers[tower_id] = TowerData(
                id=tower_id,
                type=payload.get("type", "square"),
                damage=10,
                radius=100.0,
                pos=Position(x=payload.get("x", 0), y=payload.get("y", 0))
            )

    async def run_game_loop(self, manager):
        while True:
            self.update_physics()
            await manager.broadcast(self.state.dict())
            await asyncio.sleep(self.tick_rate)

    def update_physics(self):
        enemies_to_remove = []

        for e_id, enemy in self.state.enemies.items():
            enemy.pos.x += enemy.speed

            if enemy.pos.x > 800:
                self.state.lives -= 1
                enemies_to_remove.append(e_id)

        for e_id in enemies_to_remove:
            del self.state.enemies[e_id]

    def spawn_enemy(self, enemy_type: str, hp: int, speed: float):
        enemy_id = str(uuid.uuid4())
        self.state.enemies[enemy_id] = EnemyData(
            id=enemy_id,
            type=enemy_type,
            hp=hp,
            speed=speed,
            pos=Position(x=0, y=100)
        )