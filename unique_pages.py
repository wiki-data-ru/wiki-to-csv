import wikipediaapi
import logging
import pandas as pd
from tqdm import tqdm
# import wikipedia
import requests
import json
import sys
import base64

LINKS_CSV_FILE = "./data/links_only_clear.csv"

WIKI_REQUEST = 'http://ru.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# def get_wiki_image(search_term):
#     try:
#         result = wikipedia.search(search_term, results = 1)
#         wikipedia.set_lang('ru')
#         wkpage = wikipedia.WikipediaPage(title = result[0])
#         title = wkpage.title
#         response  = requests.get(WIKI_REQUEST+title)
#         json_data = json.loads(response.text)
#         img_link = list(json_data['query']['pages'].values())[0]['original']['source']
#         return img_link        
#     except:
#         return 0
    

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

def safe_clear(df): 
    for col in df:
        if col not in ['source_name','dest_name','dest_url','source_url']:
            df = df.drop(col,axis=1)
            print("dropped ", col)
    return df

def load(): 
    links_df = pd.read_csv(LINKS_CSV_FILE)
    return links_df


def write(ldf):
    ldf.to_csv(LINKS_CSV_FILE)
    
def main():
    ldf = load()

    ldf = safe_clear(ldf)
    uniq_df=ldf["dest_name"].unique()
    src_df=ldf["source_name"].unique()
    dfu = pd.DataFrame(uniq_df)
    dfc = pd.DataFrame(src_df)

    dfu.to_csv("./dest_uniq.csv")
    dfc.to_csv("./src_uniq.csv")
    
    

if __name__ == "__main__":
    get_module_logger(__name__).info("Started parsing script")
    main()