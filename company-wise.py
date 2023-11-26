import json
from time import sleep
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

output = "company-wise.json"

links: List[str] = json.load(open("links.json"))

driver = webdriver.Chrome(
    options=Options(), service=Service(ChromeDriverManager().install())
)
driver.maximize_window()

odata = {}

for i, link in enumerate(links):
    try:
        company = link.split("/")[-1]
        print(f"{i+1}: {company}")
        driver.get(link)
        sleep(2)
        cards = driver.find_elements(By.CLASS_NAME, "ycdc-card")
        badges = driver.find_elements(By.CLASS_NAME, "ycdc-badge")

        texts = [] 
        socials = []

        infos = []

        for card in cards:
            socials_elements = card.find_elements(By.TAG_NAME, "a")
            temp_socials = {}
            for social_element in socials_elements:
                temp_socials[social_element.get_attribute("title") or ""] = social_element.get_attribute("href") or ""
            info = {
                "description": card.text,
                "socials": temp_socials,
            }
            infos.append(info)

        odata[company] = {"jobs": badges[-1].text, "data": infos}
    except:
        break
    
json.dump(odata, open(output, "w"))
