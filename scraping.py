#external imports
import requests
import pprint
import html
import urllib.parse
from bs4 import BeautifulSoup

#local imports
from database import createInstance
from database import insertProduct


base_URL = 'https://www.hannaford.com'

def insert_products(pageContent):
    product_elems = pageContent.find_all('div', class_='plp_thumb_wrap product-impressions')

    #print(product_elems)
    for product_elem in product_elems:
        name = product_elem['data-name']
        id = int(product_elem['data-id'])
        price = float(product_elem['data-price'])
        brand = product_elem['data-brand']
        category = product_elem['data-category']
        variant = product_elem['data-variant']
        dataList = product_elem['data-list']

        mydb = createInstance()
        insertProduct(mydb, id, name, price, brand, category, variant, dataList)
        mydb.close()

def scrape_page_products(URL):
    URL = URL.replace('¤', '&curren')
    page = requests.get(URL)

    #scrape the page for product names
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='pageContent')
    #hack to make show more work
    if results == None:
        results = soup

    insert_products(results)

    #see if we have a show more button, if we do get that content and parse it too
    show_more_button = results.find(id='see-more-btn')
    if show_more_button != None:
        more_URL = show_more_button['data-url']
        scrape_page_products(base_URL + more_URL)

#first, we need to scrape the category directory. This will give us links to all the pages that contain products
department_links = []

department_directory_url = 'https://www.hannaford.com/departments'
department_directory_page = requests.get(department_directory_url)
department_directory_soup = BeautifulSoup(department_directory_page.content, 'html.parser')
department_directory_page_content = department_directory_soup.find(id='main-content')
department_link_elements = department_directory_page_content.find_all('a')

for department_link_element in department_link_elements:
    href = department_link_element['href']
    if href[0:12] == '/departments':
        department_links.append("https://www.hannaford.com" + href)

category_links = []
for department_link in department_links:
    department_page = requests.get(department_link)
    department_soup = BeautifulSoup(department_page.content, 'html.parser')
    department_page_content = department_soup.find(id='main-content')
    category_link_elements = department_page_content.find_all('a')
    for category_link_element in category_link_elements:
        href = category_link_element['href']
        if href[0:12] == '/departments':
            category_links.append("https://www.hannaford.com" + href)


done_count = 0
# now scrape the category pages we found
for link in category_links:
    scrape_page_products(link)
    done_count+=1
    print("completed " + str(done_count) + " out of " + str(len(category_links)))


