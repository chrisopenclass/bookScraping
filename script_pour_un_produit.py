#importation des librairies necessaires .
from typing import ValuesView
import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/the-black-maria_991/index.html"#url de la page à parser
page = requests.get(url)#on envoi ici une requete html pour avoir le code de la page
soup = BeautifulSoup(page.content, 'html.parser')#on crée une variable dans laquel on met le code html parser

product_page_url = url# url de la page qui sera ajouté à la liste des données que l'on veut garder
#création de la liste des catégories de données que l'on veut
information = ["universal_product_code", "price_including_tax","price_excluding_tax",
               "number_avaible", "title", "product_description", "category",
               "review_rating", "image_url", "product_page_url"]
#fonction pour extraire les données de la page
def data_extraction():
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
    return donnee_livre  # on renvois notre liste  pour l'utilisé plus tard dans notre code

#on crée une variable qui sera égale au résultat de notre fonction  ( donc à une liste )
donnee_final = data_extraction()
#on ajoute l'url à la liste
donnee_final.append(url)
#on crée une liste assosiative constituée de la liste créer en début de code plus la liste des données récupérées
donne_a_sauvegarder = list(zip(information, donnee_final))

#on vérifie que nos liste ne sont pas vide avant de créer le fichier csv
if donnee_final and information and donne_a_sauvegarder is not None:
    print(donne_a_sauvegarder)
    with open('donnee_pour_un_livre.csv', 'w') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(information)
        writer.writerow(donnee_final)
#si nos listes sont vide alors on renvoi un message .
else :
    print("certaines listes sont vides")
