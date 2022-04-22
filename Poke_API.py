import requests


def get_poke_info(poke):
    
    #   Gets all of the information about a specified pokemon 
    """
    :param name: Pokemon Name
    :returns: Dictionary of Pokemon Info, if successful. Won't return anything if unsuccessful 
    """
    print("Getting Pokemon Info.....")
    pokemon = poke.lower()
    resp_msg = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon) 
    if resp_msg.status_code == 200:
        print('Success!',"\n")
        return resp_msg.json()
    else:
        print('Action Failed. Response code:', resp_msg.status_code)
        return
#   Get the image of te pokemon
def get_pokemon_image_url(name):
    pokemon_dict = get_poke_info(name)
    if pokemon_dict:
        return pokemon_dict['sprites']['other']['official-artwork']['front_default']                                                                                                                                                   
   
#   Get the list of pokemon    
def get_poke_list(limit=100, offset=0):
    url = 'https://pokeapi.co/api/v2/pokemon'
    
    params = {
        'limit': limit,
        'offset': offset
    }
    
    resp_msg = requests.get(url, params=params)
    
    if resp_msg.status_code == 200:
        print ("Success!")
        dict = resp_msg.json()
        return [p['name'] for p in dict ['results']]
    else:
        print("Failed to get Pokemon List.")
        print("Responce code:", resp_msg.status_code)
        