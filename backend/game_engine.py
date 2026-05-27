import asyncio
import uuid
import math
from models import GameState, EnemyData, TowerData, Position


class GameEngine:
    def __init__(self):
        self.state = GameState(
            money=100,
            lives=20,
            wave=1,
            enemies={},
            towers={}
        )
        self.tick_rate = 1 / 30
        self.wave_active = False

    def process_input(self, data: dict):
        action = data.get("action")
        payload = data.get("payload", {})

        if action == "place_tower":
            if self.state.money >= 50:
                self.state.money -= 50
                tower_id = str(uuid.uuid4())
                self.state.towers[tower_id] = TowerData(
                    id=tower_id,
                    type=payload.get("type", "square"),
                    damage=1,
                    radius=150.0,
                    pos=Position(x=payload.get("x", 0), y=payload.get("y", 0))
                )

        elif action == "start_wave":
            if not self.wave_active:
                self.wave_active = True
                asyncio.create_task(self.spawn_wave_routine())

    async def spawn_wave_routine(self):
        for _ in range(10):
            self.spawn_enemy("circle", 50, 2.0)
            await asyncio.sleep(2)

        self.wave_active = False
        self.state.wave += 1

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

        for t_id, tower in self.state.towers.items():
            for e_id, enemy in self.state.enemies.items():
                if e_id in enemies_to_remove:
                    continue

                dx = tower.pos.x - enemy.pos.x
                dy = tower.pos.y - enemy.pos.y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance <= tower.radius:
                    enemy.hp -= tower.damage

                    if enemy.hp <= 0 and e_id not in enemies_to_remove:
                        self.state.money += 10
                        enemies_to_remove.append(e_id)
                    break

        for e_id in set(enemies_to_remove):
            if e_id in self.state.enemies:
                del self.state.enemies[e_id]

    def spawn_enemy(self, enemy_type: str, hp: int, speed: float):
        enemy_id = str(uuid.uuid4())
        self.state.enemies[enemy_id] = EnemyData(
            id=enemy_id,
            type=enemy_type,
            hp=hp,
            speed=speed,
            pos=Position(x=0, y=300)
        )