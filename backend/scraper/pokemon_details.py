import requests
from .scraper import get_page
import typing
import re

def get_pokemon_page(pokemon_name):
    url = f"https://www.serebii.net/pokedex-sv/{pokemon_name.lower()}/"
    soup = get_page(url)
    if soup:
        print(soup.title.string)

# returns a list of tuples with Pokémon number and name
def get_all_pokemon():
    url = "https://www.serebii.net/pokemon/nationalpokedex.shtml"
    soup = get_page(url)
    if soup:
        pokemon_list = []
        dex_table = soup.find("table", {"class": "dextable"})
        for table_row in dex_table.find_all("tr")[2:]:
            cells = table_row.find_all("td")
            if len(cells) < 2:
                continue
            pokemon_list.append(cells)
        return pokemon_list

def get_pokemon_abilities():
    url = "https://www.serebii.net/games/ability.shtml"
    soup = get_page(url)
    if soup:
        abilities = []
        # Find all the ability name tags based on the user's description
        ability_name_tags = soup.find_all('td', {'colspan': '2'})
        for tag in ability_name_tags:
            a_tag = tag.find('a')
            if not (a_tag and a_tag.has_attr('name')):
                continue

            font_tag = a_tag.find('font', {'size': '4'})
            if not font_tag:
                continue

            b_tag = font_tag.find('b')
            if not b_tag:
                continue

            ability_name = b_tag.get_text(strip=True)

            # Find the description in the next row
            description_row = tag.find_parent('tr').find_next_sibling('tr')
            if description_row:
                description_cell = description_row.find('td')
                if description_cell:
                    cell_text = description_cell.get_text(separator=' ', strip=True)
                    effect_marker = "In-Battle Effect:"
                    if effect_marker in cell_text:
                        # Split the string at the marker and take the second part
                        description = cell_text.split(effect_marker, 1)[1].strip()
                        # Remove any other sections that might follow
                        if "Overworld Effect:" in description:
                            description = description.split("Overworld Effect:")[0].strip()
                        abilities.append((ability_name, description))
        return abilities

if __name__ == "__main__":
    abilities = get_pokemon_abilities()
    for ability in abilities:
        print(ability)
    


