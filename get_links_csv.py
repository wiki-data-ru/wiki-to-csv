import wikipediaapi
import logging
import pandas as pd
from tqdm import tqdm
import wikipedia
import requests
import json
import sys
import base64

LINKS_CSV_FILE = "./data/links_only.csv"

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
    

def get_as_base64(url):
    if url == 0:
        return 0 
    return base64.b64encode(requests.get(url).content)

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


def load(): 
    links_df = pd.read_csv(LINKS_CSV_FILE)
    return links_df


def write(ldf):
    ldf.to_csv(LINKS_CSV_FILE)
    
def main():
    ldf = load()

    wiki_wiki = wikipediaapi.Wikipedia('ru')
    
    page_py = wiki_wiki.page(sys.argv[1])
    
    data  = []

    source_name = page_py.title
    source_url = page_py.fullurl

    for page in tqdm(page_py.links.keys()):
        try:
            page_name = page.title
            new_row = {
                'source_name': source_name,
                'source_url': source_url,
                'dest_name': page,
                'dest_url': page_py.links[page].fullurl
            }

            data.append(new_row)

        except KeyError:
            continue
    
    data = pd.DataFrame.from_dict(data)

    frame_data = [ldf, data]

    updated_data = pd.concat(frame_data)
    write(updated_data)
    
    

if __name__ == "__main__":
    get_module_logger(__name__).info("Started parsing script")
    main()