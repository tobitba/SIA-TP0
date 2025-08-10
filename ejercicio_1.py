import json
import sys
import matplotlib.pyplot as plt

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

tiradas = 500

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    pokemones = ["jolteon", "caterpie", "snorlax", "onix", "mewtwo"]
    balls = ["pokeball", "ultraball", "fastball", "heavyball"]
    config = {"pokemon": "jolteon", "pokeball": "pokeball"}
    averages = []


    for ball in balls:
        sum = 0
        total = 0
        for i in range(tiradas, 1, -1):
            for pokemon in pokemones:
                pokemon = factory.create(pokemon, 100, StatusEffect.NONE, 1)
                catch = attempt_catch(pokemon, ball)
                if catch[0]:
                    sum += 1
                total += 1
                #print("Pokemon: {} | Catch: {}".format(pokemon.name, catch))
        average = sum / total
        averages.append(average)

        print("Average: {} for {}".format(sum / total, ball))

    colors = ["red", "gold", "green", "blue"]

    plt.bar(balls, averages, color=colors)
    plt.xlabel('Pokeball Type')
    plt.ylabel('Average Catch Rate')
    plt.title('Average Catch Rate per Ball')
    plt.ylim(0, 0.25)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, avg in enumerate(averages):
        plt.text(i, avg + 0.02, f"{avg:.2f}", ha='center', fontsize=9)

    plt.show()