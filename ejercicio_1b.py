import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

throws = 1000

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    pokemons = ["jolteon", "caterpie", "snorlax", "onix", "mewtwo"]
    balls = ["pokeball", "ultraball", "fastball", "heavyball"]

    results = defaultdict(lambda: defaultdict(list))

    for pokemon_name in pokemons:
        for ball in balls:
            for i in range(throws, 1, -1):
                pokemon = factory.create(pokemon_name, 100, StatusEffect.NONE, 1)
                catch = attempt_catch(pokemon, ball)
                results[pokemon_name][ball].append(1 if catch[0] else 0)

    relative_effectiveness = {ball: [] for ball in balls}

    for pokemon in pokemons:
        base_avg = np.mean(results[pokemon]["pokeball"])
        for ball in balls:
            avg = np.mean(results[pokemon][ball])
            relative_eff = avg / base_avg if base_avg > 0 else 0
            relative_effectiveness[ball].append(relative_eff)

    x = np.arange(len(pokemons))
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['RoyalBlue', 'MediumOrchid', 'DarkOrange', 'MediumSeaGreen']

    for i, ball in enumerate(balls):
        ax.bar(x + i * width, relative_effectiveness[ball], width, label=ball, color=colors[i])

    ax.set_xticks(x + width * (len(balls) - 1) / 2)
    ax.set_xticklabels(pokemons)
    ax.set_ylabel("Relative Effectiveness to Pokeball")
    ax.set_xlabel("Pokemon")
    ax.set_title("Comparison of Pokeball Effectiveness by Pokemon")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.ylim(0, max(max(vals) for vals in relative_effectiveness.values()) * 1.2)
    plt.savefig("ejercicio_1b.png", dpi=300)