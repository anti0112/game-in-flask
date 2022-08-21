from unit import BaseUnit
from typing import Optional, Dict, Any

STAMINA_PER_ROUND = 1.3

class BaseSingleton(type):
	_instances: Dict[Any, Any] = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
	"""Класс арены"""
	stamina_per_round = STAMINA_PER_ROUND
	user: BaseUnit
	enemy: BaseUnit
	battle_result: str = ''
	game_is_running = False

	def start_game(self, user: BaseUnit, enemy: BaseUnit):
		"""Начинает бой"""
		self.game_is_running = True
		self.user = user
		self.enemy = enemy

	def next_turn(self) -> Optional[str]:
		"""Передает ход сопернику (ПК)"""
		enemy_hit = self.enemy.hit(self.user)
		if self.is_hp_null():
			self.game_over()
		else:
			self.stamina_regeneration()
		return enemy_hit

	def stamina_regeneration(self):
		"""Восстанавливает выносливость после завершения раунда"""
		self.user.stamina = round(self.user.stamina + self.stamina_per_round * self.user.stamina_modify, 1)
		if self.user.stamina > self.user.unit_class.max_stamina:
			self.user.stamina = self.user.unit_class.max_stamina

		self.enemy.stamina = round(self.enemy.stamina + self.stamina_per_round * self.enemy.stamina_modify, 1)
		if self.enemy.stamina > self.enemy.unit_class.max_stamina:
			self.enemy.stamina = self.enemy.unit_class.max_stamina

	def is_hp_null(self) -> Optional[str]:
		"""Делает проверку HP персонажа"""
		if self.user.hp > 0 and self.enemy.hp > 0:
			return None
		elif self.user.hp > 0:
			battle_result = 'Игрок победил!'
		elif self.enemy.hp > 0:
			battle_result = 'Игрок проиграл!'
		else:
			battle_result = 'Ничья!'
		self.battle_result = battle_result
		return battle_result

	def game_over(self) -> str:
		"""Завершает игру"""
		Arena._instances = {}
		self.game_is_running = False
		return self.battle_result

	def users_hit(self) -> Optional[str]:
		"""Выполняет удар игрока"""
		return self.user.hit(self.enemy)

	def used_skill(self) -> Optional[str]:
		"""Выполняет удар ПК"""
		return self.user.get_skill_to_target(self.enemy)