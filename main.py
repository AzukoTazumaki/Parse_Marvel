import requests
import bs4
import pandas as pd

url = "https://www.marvel.com"
response = requests.get(url + "/characters")

resp_body = bs4.BeautifulSoup(response.content, "html.parser")
cards = resp_body.find("section", {"id": "content_grid-3"}).find_all("div", {"class": "mvl-card mvl-card--explore"})

character_bio = []

for card in cards:
    link = card.find("a", {"class": "explore__link"})
    character_page_resp = requests.get(url + link["href"])
    character_page = bs4.BeautifulSoup(character_page_resp.content, "html.parser")
    menu_links = character_page.find("section", {"id": "masthead-1"}).find_all(
        "a", {"class": "masthead__tabs__link"}
    )
    if len(menu_links) == 0:
        continue
    characters_in_comics_resp = requests.get(url + menu_links[-1]["href"])
    characters_in_comics_page = bs4.BeautifulSoup(characters_in_comics_resp.content, "html.parser")
    character_name = characters_in_comics_page.find("span", {"class": "masthead__headline"}).text
    bio = {
        "name": character_name,
        "link": url + link["href"]
    }
    for li in characters_in_comics_page.find_all("li", {"class": "railBioInfo__Item"}):
        bio[li.find("p").text] = li.find("li").text

    character_bio.append(bio)

df = pd.DataFrame(character_bio)
df.to_excel("results.xlsx")



