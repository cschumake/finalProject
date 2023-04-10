import requests
from anytree import Node, RenderTree

def get_pokemon(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_pokemon_species(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_evolution_chain(chain_id):
    url = f'https://pokeapi.co/api/v2/evolution-chain/{chain_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def build_evolution_tree(chain, parent=None):
    if not chain:
        return

    species = chain['species']['name']
    pokemon_data = get_pokemon(species)
    stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
    stats_str = ', '.join([f"{k}: {v}" for k, v in stats.items()])
    node = Node(f"{species} ({stats_str})", parent=parent)

    for evo in chain['evolves_to']:
        build_evolution_tree(evo, parent=node)

    return node

def main():
    while True:
        pokemon_name = input('Enter the name of a Pokemon (or type "exit" to quit): ').lower().strip()
        
        if pokemon_name == 'exit':
            break

        try:
            species = get_pokemon_species(pokemon_name)
            chain_id = species['evolution_chain']['url'].split('/')[-2]
            evolution_chain = get_evolution_chain(chain_id)

            evolution_tree = build_evolution_tree(evolution_chain['chain'])

            print(f"Evolution tree with stats for {pokemon_name}:")
            for pre, _, node in RenderTree(evolution_tree):
                print(f"{pre}{node.name}")

        except requests.exceptions.HTTPError:
            print(f"Error: '{pokemon_name}' not found. Please try again with a valid Pokemon name.")

if __name__ == '__main__':
    main()
