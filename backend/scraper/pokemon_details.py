import requests
from scraper import get_page
import typing

def get_pokemon_page(pokemon_name):
    url = f"https://www.serebii.net/pokedex-sv/{pokemon_name.lower()}/"
    soup = get_page(url)
    if soup:
        print(soup.title.string)

# returns a list of tuples with Pokémon number and name
def get_all_pokemon() -> typing.List[typing.Tuple[int, str]]:
    url = "https://www.serebii.net/pokemon/nationalpokedex.shtml"
    soup = get_page(url)
    if soup:
        pokemon_list = []
        dex_table = soup.find("table", {"class": "dextable"})
        for table_row in dex_table.find_all("tr")[2:]:
            cells = table_row.find_all("td")
            if len(cells) < 2:
                continue
            [number, pic, what, name] = cells[:4]
            pokemon_list.append((int(number.text.strip().lstrip("#")), name.text.strip()))
        return pokemon_list

if __name__ == "__main__":
    pkmn_list = get_all_pokemon()
    print(f"Found {len(pkmn_list)} Pokémon:")
    for pkmn in pkmn_list:
        print(pkmn)



