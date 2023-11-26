import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

output = "links.json"

driver = webdriver.Chrome(
    options=Options(), service=Service(ChromeDriverManager().install())
)
driver.maximize_window()
driver.get('https://www.ycombinator.com/companies')

sleep(5)

SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
sleep(10)

companies = driver.find_elements(By.CSS_SELECTOR, "a[class^='_company_']")
print("Number of companies: {}".format(len(companies)))

links = []

for company in companies:
    links.append(company.get_attribute("href"))

json.dump(links, open(output, "w"))

driver.quit()
