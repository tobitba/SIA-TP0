import plotly.graph_objects as go
import numpy as np

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

throws = 1000

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")
    pokemons = ["jolteon", "caterpie", "snorlax", "onix", "mewtwo"]
    balls = ["pokeball", "ultraball", "fastball", "heavyball"]

    averages = []
    errors = []

    for ball in balls:
        results = []
        for i in range(throws, 1, -1):
            for pokemon in pokemons:
                pokemon = factory.create(pokemon, 100, StatusEffect.NONE, 1)
                catch = attempt_catch(pokemon, ball)
                results.append(1 if catch[0] else 0)

        avg = np.mean(results)
        err = np.std(results) / np.sqrt(len(results))
        averages.append(avg)
        errors.append(err)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = balls,
        y = averages,
        error_y = dict(
            type = 'data',
            array = errors,
            visible = True
        ),
        marker = dict(color = ['RoyalBlue', 'MediumOrchid', 'DarkOrange', 'MediumSeaGreen'])
    ))

    fig.update_layout(
        title = "Average Catch Rate per Ball",
        xaxis_title = "Pokeball Type",
        yaxis_title = "Average Catch Rate",
        yaxis = dict(range = [0, 0.25]),
        bargap = 0.2,
    )

    fig.write_image("ejercicio_1a.png")