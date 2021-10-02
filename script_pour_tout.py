import requests
from bs4 import BeautifulSoup
import csv

lien_du_site = "http://books.toscrape.com/"

base_url = "http://books.toscrape.com/index.html"

index_des_categories = []
lien_de_tout = []
nombre_de_page = []

liens_a_parser = {}

information = {
    "universal_product_code" : [],
    "price_including_tax" : [],
    "price_excluding_tax" : [],
    "number_avaible" : [], 
    "title" : [],
    "product_description" : [],
    "category" : [],
    "review_rating" : [],
    "image_url" : [], 
    "product_page_url" : []
               }  

def recuperation_des_categories () :
    page = requests.get(base_url)
    index = BeautifulSoup(page.content, 'html.parser')
    for x in index.find("div", class_="side_categories").find_all("li"):
        a = x.find("a")
        if'href' in a.attrs:
            url = a.get('href')
            lien_cathegories = lien_du_site+url
            index_des_categories.append(lien_cathegories)
    del index_des_categories[0]
    return index_des_categories

recuperation_des_categories()

def parse_categories():
    for categories in index_des_categories :
        page_categories = requests.get(categories)
        if page_categories.status_code == requests.codes.ok:
            page_a_parser = BeautifulSoup(page_categories.content, "html.parser")
        find_next = page_a_parser.find("li", class_="next")
        find_previous = page_a_parser.find("li", class_="previous")
        if find_next == None :
            urls = []
            nom_de_la_categorie = page_a_parser.find("li", class_="active").text
            for lien in page_a_parser.find_all("h3"):
                a_tag = lien.find("a")
                url = a_tag.get('href').replace("../../../","http://books.toscrape.com/catalogue/")
                urls.append(url)
            liens_a_parser.update({nom_de_la_categorie:urls})
        if find_next != None or find_previous != None:
            pass

def data_extraction(item):
    items = requests.get(item)
    soup = BeautifulSoup(items.content, 'html.parser')
    donnee_livre = []
    for x in soup.findChildren(["td"]) :
        donnee_livre.append(x.string)
    information['universal_product_code'].append(donnee_livre[0])
    information['price_including_tax'].append(donnee_livre[2])
    information['price_excluding_tax'].append(donnee_livre[3])
    information['number_avaible'].append(donnee_livre[5])
    information['title'].append(soup.find("li", class_="active").string)# on ajoute le titre
    information['product_description'].append(soup.find("p", class_=False, id=False).string)# on ajoute la description du produit
    information['category'].append(soup.find("ul", class_="breadcrumb").find_all('a')[2].text)# on ajoute la catégorie
    note_du_livre = (soup.find("p", class_="star-rating").attrs)#création d'un dictionaire contenant les atributs de la balise de la note
    information['review_rating'].append(list(note_du_livre.values()))# on extrai uniquement la note qui est une valeur du dictionnaire
    information['image_url'].append(soup.find("img").get("src").replace("../../", "http://books.toscrape.com/"))#on ajoute la lien de lien de l'image
    information['product_page_url'].append(item)
    return information

parse_categories()
