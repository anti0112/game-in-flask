from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
	id: int
	name: str
	defence: float
	stamina_per_turn: float

@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def get_damage_by_weapon(self) -> float:
        """Рассчитывает случайный урон в промежутке min_damage - max_damage"""
        damage = uniform(self.min_damage, self.max_damage)
        return round(damage, 1)



@dataclass
class EquipmentData:
	weapons: List[Weapon]
	armors: List[Armor]


class Equipment:

    def __init__(self):
        self._equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        """возвращает объект оружия по имени"""
        for item in self._equipment.weapons:
            if weapon_name == item.name:
                return item
        return None


    def get_armor(self, armor_name) -> Optional[Armor]:
        """возвращает объект брони по имени"""
        for item in self._equipment.armors:
            if armor_name == item.name:
                return item
        return None
        

    def get_weapons_list(self) -> List[str]:
        """возвращаем список с оружием"""
        return [i.name for i in self._equipment.weapons]

    def get_armors_list(self) -> List[str]:
        """возвращаем список с броней"""
        return [i.name for i in self._equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        equipment_file = open("./data/equipment.json", 'r', encoding='utf-8')
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError


