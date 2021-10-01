import requests
from bs4 import BeautifulSoup
import csv

lien_du_site = "http://books.toscrape.com/"

information = {"universal_product_code" : [],
               "price_including_tax" : [],
               "price_excluding_tax" : [],
               "number_avaible" : [], 
               "title" : [],
               "product_description" : [],
               "category" : [],
               "review_rating" : [],
               "image_url" : [], 
               "product_page_url" : []} 

urls_categories = []
lien_de_tout = []
nombre_de_page = []

def recuperation_des_categories () :
    url = "http://books.toscrape.com/index.html"
    page = requests.get(url)
    index = BeautifulSoup(page.content, 'html.parser')
    for x in index.find("div", class_="side_categories").find_all("li"):
        a = x.find("a")
        try:
            if'href' in a.attrs:
                url = a.get('href')
                lien_cathegories = lien_du_site+url
                urls_categories.append(lien_cathegories)
        except:
            print("marche pas la la la" )
    del urls_categories[0]
    return urls_categories

recuperation_des_categories()

def recuperation_des_livres(urls_categories):
    liste_page = []
    urls = []
    for liens in urls_categories:
        liste_page.append(liens)
        page = requests.get(liens)
        soup = BeautifulSoup(page.content, 'html.parser')
        test = soup .find("li", class_="next")
        print(liens)
        if test == None :
            for liste_livre in liste_page :
                page_livre = requests.get(liste_livre)
                soup_de_livre = BeautifulSoup(page_livre.content, 'html.parser')
                test = soup_de_livre.select("h3 a")
                for x in soup_de_livre.find_all("h3"):
                    a = x.find("a")
                    try:
                        if'href' in a.attrs:
                            url = a.get('href').replace("../../../","http://books.toscrape.com/catalogue/")
                            urls.append(url)
                            print([data_extraction(item) for item in urls])
                    except:
                        print("marche pas la la la" )
        else:
            print(test)


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
    print(information)
    


recuperation_des_livres(urls_categories)






