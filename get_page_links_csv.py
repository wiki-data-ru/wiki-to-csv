import wikipediaapi
import logging
import pandas as pd
from tqdm import tqdm
import wikipedia
import requests
import json
import sys
import base64

LINKS_CSV_FILE = "./data/links.csv"
PAGES_CSV_FILE = "./data/pages.csv"

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
    pages_df = pd.read_csv(PAGES_CSV_FILE)
    return links_df, pages_df


def write(pdf, ldf):
    pdf.to_csv(PAGES_CSV_FILE)
    ldf.to_csv(LINKS_CSV_FILE)
    
def main():
    ldf, pdf = load()

    wiki_wiki = wikipediaapi.Wikipedia('ru')
    
    page_py = wiki_wiki.page(sys.argv[1])
    
    pages = []
    links = []

    for page in tqdm(page_py.links.keys()):
        try:
            page_name = page
            page_desc = page_py.links[page].summary
            page_url = page_py.links[page].fullurl
            new_row = {
                'title': page_name,
                'desc': page_desc,
                'url': page_url,
                'img': get_as_base64(get_wiki_image(page_name))
            }
            get_module_logger(__name__).info(f'Added {new_row}')

            pages.append(new_row)

            links.append({'source': page_py.title,'dest': new_row['title']})

        except KeyError:
            continue
    
    new_ldf = pd.DataFrame.from_dict(links)
    new_pdf = pd.DataFrame.from_dict(pages)

    frame_links = [ldf, new_ldf]
    frame_pages = [pdf, new_pdf]

    new_links = pd.concat(frame_links)
    new_pages = pd.concat(frame_pages)
    write(new_pages, new_links)
    # write(new_pdf, new_ldf)
    
    

if __name__ == "__main__":
    get_module_logger(__name__).info("Started parsing script")
    main()