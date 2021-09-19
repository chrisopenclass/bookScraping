import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/the-black-maria_991/index.html"
page = requests.get(url)
print (page)
soup = BeautifulSoup(page.content, 'html.parser')

product_page_url = url
information = ["universal_product_code", "price_including_tax", "number_avaible",
               "price_excluding_tax", "title", "product_description", "category",
               "review_rating", "image_url", "product_page_url"]

def data_extraction():
    donnee_livre = []
    donnee_livre = soup.findChildren(["td"])
    del donnee_livre[1]
    del donnee_livre[3]
    del donnee_livre[4]
    donnee_livre.append(soup.find("li", class_="active").string)
    donnee_livre.append(soup.find("p", class_=False, id=False).string)
    donnee_livre.append(soup.find("ul", class_="breadcrumb").find_all('a')[2].text)
    donnee_livre.append(soup.find("p", class_="star-rating").attrs)
    donnee_livre.append(soup.find("img"))
    return (donnee_livre)

donnee_final = data_extraction()
donnee_final.append(url)

donne_a_sauvegarder = list(zip(information, donnee_final))

print (donnee_final)