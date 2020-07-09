from flask import render_template;
from DB.pokemon import get_id;

def get_picture(pokemon_name):
    return render_template("/view_pok.html", name= pokemon_name, the_url= f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{get_id(pokemon_name)}.png")


def evolve_pic(pokemon_name, new_name):
    if new_name:
        return render_template("/evolve_render.html", name= pokemon_name, old_url= f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{get_id(pokemon_name)}.png", new_url= f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{get_id(new_name)}.png")
    else :
        return render_template("/evolve_render.html", name= pokemon_name, old_url= f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{get_id(pokemon_name)}.png", new_url= f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{get_id(pokemon_name)}.png")
