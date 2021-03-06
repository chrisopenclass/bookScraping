import requests
from bs4 import BeautifulSoup
import csv
import os
import time

lien_du_site = "http://books.toscrape.com/"

field_name = {
    "universal_product_code": "",
    "price_including_tax" : "" ,
    "price_excluding_tax" : "",
    "number_avaible" : "",
    "title" : "",
    "product_description" : "",
    "category" : "" ,
    "review_rating" : "",
    "image_url" : "",
    "product_page_url" : "",
    }

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
    soup = parser(lien_du_site)
    for x in soup.find("div", class_="side_categories").find_all("li"):
        a = x.find("a")
        if'href' in a.attrs:
            url = a.get('href')
            cat_url = lien_du_site+url
            url_categories.append(cat_url)
    del url_categories[0]
    print ("récupération des catégories terminée")
    return url_categories

def parse_categories(liste_cat):
    print("début de la récupération des livres")
    dic = {}
    for item in liste_cat:
        url_categorie = item
        soup = parser(url_categorie)
        find_next = soup.find("li", class_="next")
        if not soup.find("li", class_="next") :
            final_categories_list = soup.find("h1").string
            soup_cat = parser(url_categorie)
            liste_de_la_categorie = soup_cat.findChildren("h3")
            liste_des_liens =[]
            for i in liste_de_la_categorie :
                les_liens = i.find("a").get('href').replace("../../../", book_base_url)
                liste_des_liens.append(les_liens)
            dic[final_categories_list]=(liste_des_liens)
        else :
            final_categories_list = soup.find("h1").string
            dic[final_categories_list] = [url_categorie]
            page = 0
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
                    dic[final_categories_list].remove(url_categorie)
                    break
    print ("récupération des livres terminée")
    return dic

def book_download (titre ,img_url):
    name = str(titre)
    lien = img_url.split()
    with open(f"{name.replace(' ', '_')}.jpg", "wb") as img:
        for url in lien :
            img.write(requests.get(url).content)
    return True

def data_extraction(item):
    information = {}
    donnee_livre = []
    soup = parser(item)
    for x in soup.findChildren(["td"]) :
        donnee_livre.append(x.string)
    information['universal_product_code']=(donnee_livre[0])
    information['price_including_tax']=(donnee_livre[2])
    information['price_excluding_tax']=(donnee_livre[3])
    information['number_avaible']=(donnee_livre[5])
    information['title']=(soup.find("li", class_="active").string)
    titre = (donnee_livre[0])
    if soup.find("p", class_=False, id=False):
        information['product_description']=(soup.find("p", class_=False, id=False).string)
    else:
        information['product_description']=("ce produit n'as pas de description")
    information['category']=(soup.find("ul", class_="breadcrumb").find_all('a')[2].text)
    note_du_livre = soup.find(class_='star-rating')
    information['review_rating']=(note_du_livre['class'][1])
    information['image_url']=(soup.find("img").get("src").replace("../../", "http://books.toscrape.com/"))
    img_url = soup.find("img").get("src").replace("../../", "http://books.toscrape.com/")
    img_url = img_url.replace('/n','')
    information['product_page_url']=(item)
    book_download (titre, img_url)
    return information

def creation_du_dossier(directory):
    try:
        os.mkdir(directory)
    except PermissionError:
        print(f"Impossible de créer le dossier'{directory}' !")
        print("permission refusé")
        exit()

def main (param):
    for keys, values in param.items():
        categorie = keys
        livres = values
        print("début de la récupération des information de la catégorie " + categorie)
        creation_du_dossier(categorie)
        os.chdir(categorie)
        with open(f'{categorie}.csv', 'w',encoding="utf-8", newline='') as fichier_csv:
            writer = csv.DictWriter(fichier_csv,delimiter=',', fieldnames=field_name.keys())
            writer.writeheader()
            for data in livres : 
                data_list = data
                donnee = data_extraction(data_list)
                writer.writerow(donnee)
        print("récupération des données de la catégories " + categorie + " téminé")
        os.chdir("../")
    print("récupération compléte terminée")
        
recup_cat = recuperation_des_categories()
recup_livre = parse_categories(recup_cat)
main(recup_livre)