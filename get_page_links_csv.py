import wikipediaapi
import logging
import pandas as pd
from tqdm import tqdm
import wikipedia
import requests
import json
import sys



WIKI_REQUEST = 'http://ru.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('ru')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0
    

def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def main():
    wiki_wiki = wikipediaapi.Wikipedia('ru')
    
    page_py = wiki_wiki.page(sys.argv[1])
    
    rows = []

    for page in tqdm(page_py.links.keys()):
        try:
            page_name = page
            page_desc = page_py.links[page].summary
            page_url = page_py.links[page].fullurl
            new_row = {
                'title': page_name,
                'desc': page_desc,
                'url': page_url,
                'img': get_wiki_image(page_name)
            }
            get_module_logger(__name__).info(f'Added {new_row}')
            rows.append(new_row)
            wiki_df = pd.DataFrame.from_dict(rows)
            wiki_df.to_csv(f'data/{sys.argv[1]}_links.csv')
        except KeyError:
            continue
    
    

if __name__ == "__main__":
    get_module_logger(__name__).info("Started parsing script")
    main()