import requests
from bs4 import BeautifulSoup
import csv

lien_du_site = "http://books.toscrape.com/"

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
    donnee_livre = []#on initialise une liste vide qui va nous servir
    for x in soup.findChildren(["td"]) :# boucle pour ajouter les 4 premiéres données recherché sans les balises à notre liste
        donnee_livre.append(x.string)
    #suppression des données non voulu
    del donnee_livre[1]
    del donnee_livre[3]
    del donnee_livre[4]
    donnee_livre.append(soup.find("li", class_="active").string)# on ajoute le titre
    donnee_livre.append(soup.find("p", class_=False, id=False).string)# on ajoute la description du produit
    donnee_livre.append(soup.find("ul", class_="breadcrumb").find_all('a')[2].text)# on ajoute la catégorie
    note_du_livre = (soup.find("p", class_="star-rating").attrs)#création d'un dictionaire contenant les atributs de la balise de la note
    cle_a_garder = list(note_du_livre.values())# on extrai uniquement la note qui est une valeur du dictionnaire
    donnee_livre.append(cle_a_garder)#on ajoute la note
    donnee_livre.append(soup.find("img").get("src").replace("../../", "http://books.toscrape.com/"))#on ajoute la lien de lien de l'image
    donnee_livre.append(item)
    return donnee_livre  # on renvois notre liste  pour l'utilisé plus tard dans notre code


recuperation_des_livres(urls_categories)






