import requests as req
import pandas as pd
from services.json_service import load_json
from services.plot_service import plot_bar 
from bs4 import BeautifulSoup
from random import randint
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}

page_number_pattern = '{PAGE_NUMBER}'

url_config = load_json('url_config.json')

data = []
for region, url in url_config.items():
    url = url.replace(page_number_pattern, '0')
    print('Loading recipes for the following region:', region, f'({url})')

    page = req.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    total_recipes_str = soup.find('span', {'class': 'ds-h7'}).text
    total_recipes_str = total_recipes_str.replace('Ergebnisse', '').replace('Ergebnis', '').replace('.', '')
    total_recipes_str = total_recipes_str.strip()
    total_recipes = int(total_recipes_str)

    recipe_urls = []
    recipes = soup.find_all('article', {'class': 'rsel-item'})
    
    for recipe in recipes:
        recipe_url = recipe.find('a', {'class': 'rsel-recipe'}, href=True)['href']
        recipe_urls.append(recipe_url)
    
    data.append([region, total_recipes, recipe_urls])
    sleep(randint(100,750) / 1000) # wait between 0.1 and 0.75 seconds before requesting the next page

df = pd.DataFrame(data, columns = ['Region', 'AmountOfRecipes', 'FirstPageRecipes'])
plot_bar(df, 'Region', 'AmountOfRecipes', 'Amount of vegan recipes by region (chefkoch.de)', "Region", "Amount of recipes", save_as="graphics/chefkoch_de.png")