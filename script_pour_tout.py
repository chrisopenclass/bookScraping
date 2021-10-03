import requests
from bs4 import BeautifulSoup
import csv
import os

lien_du_site = "http://books.toscrape.com/"

base_url = "http://books.toscrape.com/index.html"

book_base_url = "http://books.toscrape.com/catalogue/"

def parser(url):
    try:
        reponse = requests.get(url)
    except:
        print ("l'url n'est pas valide")
        os._exit(1)
    if reponse.status_code == requests.codes.ok:
        soup = BeautifulSoup(reponse.content, "html.parser")
        return soup
    else :
        soup = None
        return soup

def recuperation_des_categories () :
    url_categories = []
    soup = parser(base_url)
    for x in soup.find("div", class_="side_categories").find_all("li"):
        a = x.find("a")
        if'href' in a.attrs:
            url = a.get('href')
            cat_url = lien_du_site+url
            url_categories.append(cat_url)
    del url_categories[0]
    return url_categories

list_cat = recuperation_des_categories()

def parse_categories(liste_cat):
    dic = {}
    for item in liste_cat:
        url_categorie = item
        soup = parser(url_categorie)
        find_next = soup.find("li", class_="next")
        if not soup.find("li", class_="next") :
            k_categories = url_categorie.replace("http://books.toscrape.com/catalogue/category/books/", " ")
            final_categories_list = k_categories.replace("/index.html", " ")
            dic[final_categories_list] = [""]
            soup_cat = parser(url_categorie)
            soup_catcat = soup_cat.find("ol", class_="row")
            liste_de_la_categorie = soup_catcat.findChildren("h3")
            for i in liste_de_la_categorie :
                les_liens = i.find("a").get('href').replace("../../../", book_base_url)
                dic[final_categories_list].append(les_liens)
        else :
            k_categories = url_categorie.replace("http://books.toscrape.com/catalogue/category/books/", " ")
            final_categories_list = k_categories.replace("/index.html", " ")
            dic[final_categories_list] = [url_categorie]
            page = 0
            li = []
            while find_next :
                page += 1
                pagination = (f"page-{page}.html")
                construction_de_lurl = item.replace("index.html", pagination)
                soup2 = parser(construction_de_lurl)
                if soup2 != None :
                    liste_des_livres = soup2.find("ol", class_="row")
                    book_list = liste_des_livres.findChildren("h3")
                    for i in book_list :
                        url_book = i.find("a").get('href').replace("../../../", book_base_url)
                        dic[final_categories_list].append(url_book)
                    find_next = url_book
                else :
                    break
    return dic

dic_cat = parse_categories(list_cat)

print (dic_cat)

def data_extraction(item):
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
    donnee_livre = []
    for i in liste :
        soup = parser(i)
        for x in soup.findChildren(["td"]) :
            donnee_livre.append(x.string)
        information['universal_product_code'].append(donnee_livre[0])
        information['price_including_tax'].append(donnee_livre[2])
        information['price_excluding_tax'].append(donnee_livre[3])
        information['number_avaible'].append(donnee_livre[5])
        information['title'].append(soup.find("li", class_="active").string)# on ajoute le titre
        information['product_description'].append(soup.find("p", class_=False, id=False).string)# on ajoute la description du produit
        information['category'].append(soup.find("ul", class_="breadcrumb").find_all('a')[2].text)# on ajoute la catégorie
        note_du_livre = soup.find(class_='star-rating')#création d'un dictionaire contenant les atributs de la balise de la note
        information['review_rating'].append(note_du_livre['class'][1])# on extrai uniquement la note qui est une valeur du dictionnaire
        information['image_url'].append(soup.find("img").get("src").replace("../../", "http://books.toscrape.com/"))#on ajoute la lien de lien de l'image
        information['product_page_url'].append(item)
    return information
