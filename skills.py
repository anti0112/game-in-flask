from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from unit import BaseUnit


class Skill(ABC):
	_name: str
	_damage: float
	_need_stamina: float

	@abstractmethod
	def _skill_effect(self, *args):
		pass

	def use(self, unit, target) -> str:
		"""Использует умение"""
		if unit.stamina >= self._need_stamina:
			self._skill_effect(target)
			unit._is_used_skill = False
			return f'{unit.name} использует {self._name} и наносит {self._damage} урона сопернику. '
		return f'{unit.name} попытался использовать {self._name}, но у него не хватило выносливости. '


class InvisibleArrow(Skill):
	_name = 'Незаметная стрела'
	_damage = 10
	_need_stamina = 5

	def _skill_effect(self, target):
		"""Наносит урон сопернику"""
		target.get_self_damage(self._damage)


class TemperedSword(Skill):
	_name = 'Закаленный меч'
	_damage = 15
	_need_stamina = 10

	def _skill_effect(self, target):
		"""Наносит урон сопернику"""
		target.get_self_damage(self._damage)

class SparklingRain(Skill):
	_name = 'Сверкающий дождь'
	_damage = 12
	_need_stamina = 8

	def _skill_effect(self, target):
		"""Наносит урон сопернику"""
		target.get_self_damage(self._damage)