from typing import List, Optional
from models.movement import Movement, MovementKind
from models.pokemon_type import PokemonType
import random


class Pokemon:

    # Values used to calculate Pokemon base stats
    IV = 30
    EV = 85
    SAME_TYPE_ATTACK_BONUS = 1.5  # Stands for "Same-type attack bonus"
    LEVEL = 50

    def __init__(
        self,
        name: str,
        type1: PokemonType,
        type2: Optional[PokemonType],
        hp: int,
        attack: int,
        defense: int,
        sp_attack: int,
        sp_defense: int,
        speed: int,
        moves: List[Movement],
    ):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.max_hp = hp + Pokemon.IV*0.5 + Pokemon.EV *0.125 + 60
        self.hp = self.max_hp
        self.attack = attack + Pokemon.IV*0.5 + Pokemon.EV *0.125 + 5
        self.defense = defense + Pokemon.IV*0.5 + Pokemon.EV *0.125 + 5
        self.sp_attack = sp_attack + Pokemon.IV*0.5 + Pokemon.EV *0.125 + 5
        self.sp_defense = sp_defense + Pokemon.IV*0.5 + Pokemon.EV *0.125 + 5
        self.speed = speed + Pokemon.IV*0.5 + Pokemon.EV *0.125 + 5
        self.n_attack_modifier = 0
        self.n_defense_modifier = 0
        self.n_sp_attack_modifier = 0
        self.n_sp_defense_modifier = 0
        self.n_speed_modifier = 0
        self.n_accuracy_modifier = 0
        self.moves = moves

    def receive_damage(self, damage: int):
        self.hp = self.hp - damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0


def select_move(attacker: Pokemon, defender: Pokemon):
    return random.choice(attacker.moves)


class Team:

    def __init__(self, pokemons: List[Pokemon], name: str):
        self.pokemons = pokemons
        self.name = name
        self.move_selector = select_move

    def is_defeated(self):
        return all(not pokemon.is_alive() for pokemon in self.pokemons)

    def get_pokemon(self):
        for pokemon in self.pokemons:
            if pokemon.is_alive():
                return pokemon

    def count_alive_pokemons(self):
        return sum(pokemon.is_alive() for pokemon in self.pokemons)

    def set_select_move(self, move_selector: callable):
        self.move_selector = move_selector

    def reset_team(self):
        for pokemon in self.pokemons:
            pokemon.hp = pokemon.max_hp
            pokemon.n_attack_modifier = 0
            pokemon.n_defense_modifier = 0
            pokemon.n_sp_attack_modifier = 0
            pokemon.n_sp_defense_modifier = 0
            pokemon.n_speed_modifier = 0
            pokemon.n_accuracy_modifier = 0

    def is_valid_team(self):
        has_right_number_of_pokemons = len(self.pokemons) == 6
        has_right_number_of_movements = all(len(pokemon.moves) == 4 for pokemon in self.pokemons)
        has_valid_move_selector = self.check_move_selector()
        return all([has_right_number_of_pokemons, has_right_number_of_movements, has_valid_move_selector])

    def check_move_selector(self) -> bool:
        pokemon1_movements = [
            Movement("dummy1", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
            Movement("dummy2", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
            Movement("dummy3", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
            Movement("dummy4", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
        ]
        pokemon2_movements = [
            Movement("dummy5", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
            Movement("dummy6", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
            Movement("dummy7", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
            Movement("dummy8", "dummy", PokemonType.NORMAL, MovementKind.PHYSICAL, 100, "100%", 100),
        ]
        dummy_pokemon1 = Pokemon("dummy", PokemonType.NORMAL, None, 100, 100, 100, 100, 100, 100, pokemon1_movements)
        dummy_pokemon2 = Pokemon("dummy2", PokemonType.NORMAL, None, 100, 100, 100, 100, 100, 100, pokemon2_movements)
        movement = self.move_selector(dummy_pokemon1, dummy_pokemon2)
        return movement in pokemon1_movements
