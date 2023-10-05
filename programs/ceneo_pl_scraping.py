from bs4 import BeautifulSoup
import requests

# Ceneo Scraper

def sort_by_lowest_price(url_item:str) -> dict:
    """This Function Scraping Ceneo.pl For Store Name And The Price Of Searched Item
    And Return Dict With Sorted Price In Stores 

    Args:
        url_item (str): Url To Searched Item

    Returns:
        dict: Sorted Stores By Price
    """

    # Checks is url is not empty, if is empty return str info
    if url_item == '':
        return 'Empty Field'
    
    page_to_scrape = requests.get(url_item)
    soup = BeautifulSoup(page_to_scrape.text, 'lxml')

    
    product_name = soup.find('h1', class_='product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor')

    stores_data = {}

    # Checks is it a good url, if not return str info
    if product_name is None:
        return 'Wrong Url'

    stores = soup.find_all('li', class_='product-offers__list__item js_productOfferGroupItem')

    for store in stores:
        
        store_info = store.find('img', attrs="class, alt", class_= 'js_lazy')
        store_name = store_info.attrs['alt']

        store_url_info = store.find('a', attrs="class, href", class_= 'store-logo go-to-shop')

        if store_url_info is None:
            continue

        product_url_info = store_url_info.attrs['href']
        product_url = 'https://www.ceneo.pl/' + product_url_info

        store_price_info = store.find('span', class_='price')
        store_price = str(store_price_info.text).replace(',','.').replace(' ','')
        

        stores_data[float(store_price)] = {
            'store_name': store_name,
            'link': product_url
        }

        
        
        
       

    stores_sorted_data= dict(sorted(stores_data.items(), key=lambda x: x[0]))
    product_data = {product_name.text: stores_sorted_data}

    return product_data


def two_items_from_one_store(stores1:dict, stores2:dict) -> dict:
    """This Function Get 2 Dict And Checks If Are The Same Keys

    Args:
        stores1 (dict): Firest Dict To Search
        stores2 (dict): Secound Dict To Serarch

    Returns:
        dict: Sorted Dict By Values
    """

    # Temporary dict with date from stores 1
    temp_stores_data = {}

    for _, temp_data in stores1.items():
        for price, store_data in temp_data.items():
            # Adding to temp stores data store name and price
            temp_stores_data[store_data['store_name']] = price


    # Dict for store name and price
    stores_data = {}

    for _, temp_data in stores2.items():
        for price, data in temp_data.items():
            if temp_stores_data.get(data['store_name']) == None:
                continue
            else:
                stores_data[data['store_name']] = price



    for _, temp_data in stores1.items():
        for price, data in temp_data.items():
            if stores_data.get(data['store_name']) == None:
                continue
            else:
                stores_data[data['store_name']] += price


    stores_sorted_data = dict(sorted(stores_data.items(), key=lambda x: x[1]))

    return stores_sorted_data


# url1 = 'https://www.ceneo.pl/144699712'
# url2 = 'https://www.ceneo.pl/134654560'

