from flask import Flask, render_template, request, redirect
from classes import unit_classes
from equipment import Equipment
from base import Arena
from unit import BaseUnit, UserUnit, EnemyUnit

app = Flask(__name__)

heroes = {
	"player": BaseUnit,
	"enemy": BaseUnit
}

arena = Arena()
equipment = Equipment()


@app.route('/')
def index():
	"""Главная страница"""
	return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
	"""Страница выбора героя"""
	if request.method == 'GET':
		result = {
			'classes': unit_classes.keys(),
			'weapons': equipment.get_weapons_list(),
			'armors': equipment.get_armors_list()
		}
		return render_template('hero_choosing.html', result=result)

	elif request.method == 'POST':
		result = dict(request.form)
		heroes['player'] = UserUnit(
			name=result.get('name'),
			unit_class=unit_classes[result.get('unit_class')]
		)
		weapon = equipment.get_weapon(result.get('weapon'))
		armor = equipment.get_armor(result.get('armor'))
		heroes['player'].equip_weapon(weapon)
		heroes['player'].equip_armor(armor)
		return redirect('/choose-enemy/')


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
	"""Страница выбора соперника"""
	if request.method == 'GET':
		result = {
			'classes': unit_classes.keys(),
			'weapons': equipment.get_weapons_list(),
			'armors': equipment.get_armors_list()
		}
		return render_template('hero_choosing.html', result=result)

	elif request.method == 'POST':
		result = dict(request.form)
		heroes['enemy'] = EnemyUnit(
			name=result.get('name'),
			unit_class=unit_classes[result.get('unit_class')]
		)
		weapon = equipment.get_weapon(result.get('weapon'))
		armor = equipment.get_armor(result.get('armor'))
		heroes['enemy'].equip_weapon(weapon)
		heroes['enemy'].equip_armor(armor)
		return redirect('/fight/')


@app.route("/fight/")
def start_fight():
	"""Начало битвы"""
	arena.start_game(user=heroes.get('player'), enemy=heroes.get('enemy'))
	return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
	"""Нанесение удара"""
	result, battle_result = '', ''
	if arena.game_is_running:
		result = arena.users_hit()
	if arena.is_hp_null():
		battle_result = arena.game_over()
	else:
		result += arena.next_turn()
		battle_result = arena.battle_result
	return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/use-skill")
def use_skill():
	"""Использование умения"""
	result, battle_result = '', ''
	if arena.game_is_running:
		result = arena.used_skill()
	if arena.is_hp_null():
		battle_result = arena.game_over()
	if result:
		result += arena.next_turn()
		battle_result = arena.battle_result
	elif not result and not battle_result:
		result = 'Навык уже использован'
	return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
	"""Пропуск хода"""
	if arena.game_is_running:
		result, battle_result = arena.next_turn(), ''
	else:
		result, battle_result = '', arena.game_over()
	return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/end-fight")
def end_fight():
	"""Завершение боя"""
	arena.battle_result = ''
	return redirect('/')


if __name__ == "__main__":
	app.run(debug=True, port=5555)
