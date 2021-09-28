import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/category/books/childrens_11/index.html"
page = requests.get(url)
super_soup = BeautifulSoup(page.content, 'html.parser')

nombre_de_page = super_soup.find("li", class_="next").find_all("a", href=True)
base_url = "http://books.toscrape.com/catalogue/category/books/childrens_11/"

information = ["universal_product_code", "price_including_tax","price_excluding_tax",
               "number_avaible", "title", "product_description", "category",
               "review_rating", "image_url", "product_page_url"]

urls = []

lien_du_livre = []

for link in nombre_de_page:
    liste_page = []
    liste_page.append(base_url+"index.html")
    liste_page.append(base_url+link["href"])
    for liste_livre in liste_page :
        page_livre = requests.get(liste_livre)
        soup_de_livre = BeautifulSoup(page_livre.content, 'html.parser')
        test = soup_de_livre.select("h3 a")
        for x in soup_de_livre.find_all("h3") :
            a = x.find("a")
            try:
                if'href' in a.attrs:
                    url = a.get('href').replace("../../../","http://books.toscrape.com/catalogue/")
                    urls.append(url)
            except:
                print("marche pas la la la" )

for lien in urls :
    lien_du_livre.append(lien)

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

donnee_final = [data_extraction(item) for item in lien_du_livre]

with open('donnee_pour_des_livres.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(information)
    for data in donnee_final :
        donnee_a_ecrire = data
        writer.writerow(donnee_a_ecrire)
