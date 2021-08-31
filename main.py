import requests as req
import pandas as pd
import progressbar as pb
from services.json_service import load_json, load_proxies
from services.plot_service import plot_bar
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}

page_number_pattern = '{PAGE_NUMBER}'

url_config = load_json('url_config.json')
#proxies = load_proxies(headers, False)

data = []

bar = pb.ProgressBar(maxval=len(url_config.items()), widgets=[pb.Timer(), '  -  ', pb.Percentage(), '  -  ', pb.Bar('#', '[', ']')], redirect_stdout=True)
bar.start()
for index, region in enumerate(url_config):
    bar.update(index) 
    print(f'[{index}]\tLoading recipes for the following region:', region)

    url = url_config[region]
    url = url.replace(page_number_pattern, '0')

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
    sleep(randint(250,750) / 1000) # wait between 0.25 and 0.75 seconds before requesting the next page
    
bar.finish()

df = pd.DataFrame(data, columns = ['Region', 'AmountOfRecipes', 'FirstPageRecipes'])
plot_bar(df, 'Region', 'AmountOfRecipes', 'Amount of vegan recipes by region (chefkoch.de)', 'Region', 'Amount of recipes', save_as='graphics/chefkoch_de.png')