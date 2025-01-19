from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv



def scrap(url, name):
    driver = webdriver.Chrome() 
    driver.get(url)
    time.sleep(5)

    button = driver.find_element(By.CSS_SELECTOR, '.absolute.right-0.top-2\\/4.h-6.w-6.-translate-y-2\\/4.cursor-pointer.border-0.bg-transparent.p-0')
    button.click()
    time.sleep(2)
    button = driver.find_element(By.ID, 'tab1')
    button.click()
    time.sleep(2)
    #element_Source = driver.find_element("id","panel1").get_attribute("outerHTML")
    elementSourceStart=driver.page_source.find("class=\"flex flex-wrap gap-2\"") 
    elementSourceEnd=driver.page_source.find("class=\"mt-5\"")
    code=driver.page_source[elementSourceStart:elementSourceEnd]
    with open("parser\scraped_data.csv", "w", encoding="utf-8") as file:
        file.write(code)
    driver.quit()
    html_content = code
    soup = BeautifulSoup(html_content, "html.parser")
    ingredients = soup.select("a[title]")

    with open(f"recipes\{name}.csv", "w", encoding="utf-8",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ингредиент","Количество"])
        for ing in ingredients:
            name_title = ing["title"]
            amount = ing.select_one('p').text.replace("x","")
            writer.writerow([name_title, amount])
    print("Данные спизжены")
    
scrap("https://stalcraft.wiki/items/weapon/5ldkg", "АКМ")
    
    