import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

throws_per_point = 10
noise_level = 0.15
hp_point = np.linspace(0, 1, 200)

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    pokemons = ["jolteon", "snorlax"]
    ball = "fastball"
    status = StatusEffect.NONE
    level = 100

    data = []

    for pokemon_name in pokemons:
        for hp_percent in hp_point:
            for i in range(throws_per_point):
                pokemon = factory.create(pokemon_name, level, status, hp_percent)
                _, capture_rate = attempt_catch(pokemon, ball, noise = noise_level)
                data.append({
                    "hp_percent": hp_percent * 100,
                    "capture_rate": capture_rate,
                    "pokemon": pokemon_name.capitalize()
                })

    df = pd.DataFrame(data)

    plt.figure(figsize=(12, 7))
    df["hp_lost_percent"] = 100 - df["hp_percent"]
    sns.lineplot(data=df, x="hp_lost_percent", y="capture_rate", hue="pokemon", errorbar='sd')
    plt.legend(title='pokemon', loc='upper left')
    plt.title(f"Capture probability vs % HP lost for {pokemons[0].capitalize()} and {pokemons[1].capitalize()} using {ball.capitalize()}")
    plt.xlabel("% lost HP")
    plt.ylabel("Capture probability")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()