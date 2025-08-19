import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

throws = 500

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    pokemons = ["jolteon", "caterpie", "snorlax", "onix", "mewtwo"]
    ball = "pokeball"
    status_effects = [
        StatusEffect.NONE,
        StatusEffect.POISON,
        StatusEffect.BURN,
        StatusEffect.PARALYSIS,
        StatusEffect.SLEEP,
        StatusEffect.FREEZE,
    ]

    results = defaultdict(lambda: defaultdict(list))

    for pokemon_name in pokemons:
        for status in status_effects:
            for i in range(throws, 1, -1):
                pokemon = factory.create(pokemon_name, 100, status, 1)
                catch = attempt_catch(pokemon, ball)
                results[pokemon_name][status].append(1 if catch[0] else 0)

    relative_effectiveness = {status.name: [] for status in status_effects}

    for pokemon_name in pokemons:
        base_avg = np.mean(results[pokemon_name][StatusEffect.NONE])
        for status in status_effects:
            avg = np.mean(results[pokemon_name][status])
            relative_eff = avg / base_avg if base_avg > 0 else 0
            relative_effectiveness[status.name].append(relative_eff)

    x = np.arange(len(pokemons))
    width = 0.13

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["grey", "purple", "orange", "yellowgreen", "cyan", "blue"]

    for i, status in enumerate(status_effects):
        ax.bar(x + i * width, relative_effectiveness[status.name], width, label=status.name, color=colors[i])

    ax.set_xticks(x + width * (len(status_effects) - 1) / 2)
    ax.set_xticklabels(pokemons)
    ax.set_ylabel("Relative Effectiveness to None Status")
    ax.set_xlabel("Pokemon")
    ax.set_title("Relative Effectiveness of Pokeball by Pokemon Status Effect")
    ax.legend(title="Status")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylim(0, max(max(vals) for vals in relative_effectiveness.values()) * 1.2)

    plt.savefig("ejercicio_2a.png", dpi=300)