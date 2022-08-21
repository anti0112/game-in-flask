from dataclasses import dataclass
from skills import Skill, InvisibleArrow, TemperedSword, SparklingRain


@dataclass
class UnitClass:
	name: str
	max_health: float
	max_stamina: float
	attack: float
	stamina: float
	armor: float
	skill: Skill


ArcherClass = UnitClass(
	name='Лучник',
	max_health=80.0,
	max_stamina=50.0,
	attack=0.8,
	stamina=0.9,
	armor=1.2,
	skill=InvisibleArrow()
	)

KnightClass = UnitClass(
	name='Рыцарь',
	max_health=100.0,
	max_stamina=100.0,
	attack=1.5,
	stamina=0.8,
	armor=1.0,
	skill=TemperedSword()
	)
	
CatalystClass = UnitClass(
	name='Катализатор',
	max_health=90.0,
	max_stamina=80.0,
	attack=1.0,
	stamina=1.8,
	armor=1.0,
	skill=SparklingRain()
	)

unit_classes = {
	ArcherClass.name: ArcherClass,
	KnightClass.name: KnightClass,
    CatalystClass.name: CatalystClass
}
