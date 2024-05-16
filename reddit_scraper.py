import bs4
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import threading
import requests
import uuid
def extract_title_and_text(post_link):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    webdata = bs4.BeautifulSoup(requests.get(post_link, headers=headers).content, 'html.parser')

    post_title = webdata.find(slot="title").text # this IS the title
    text_section = webdata.find_all(slot="text-body") #this is not the text but rather the section, special things need to be done
    text_section_bs4 = bs4.BeautifulSoup('\n'.join(map(str, text_section)), "html.parser")
    text_section_div = text_section_bs4.find(class_="md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")
    
    text_content = []

    for i in text_section_div.contents:
        b = str(i).replace("<p>", "").replace("</p>", "")
        text_content.append(b)
    return post_title, text_content


def scrape_reddit(scroll_amount=7):
    """
    Defaults to AITA until I can add support for all reddit posts

    The more you add to scroll amount the more posts the scraper collects
    
    If you run it multiple times it will scrape the same posts from top to bottom
    """
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get('https://www.reddit.com/r/AmItheAsshole/')

    last_height = browser.execute_script("return document.body.scrollHeight")
    for i in range(scroll_amount):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    html_source_code = browser.execute_script("return document.body.innerHTML;")
    webdata = bs4.BeautifulSoup(html_source_code, 'html.parser')
    back = webdata.find_all('a', slot="full-post-link")
    back.pop(0)
    print(len(back))
    for i in back:
        post_link = f"https://www.reddit.com{i['href']}"
        data_back_title, data_back_content = extract_title_and_text(post_link)

        uid = uuid.uuid4()
        #clean content
        for y in data_back_content:
            y.replace("</li>", "").replace("<li>", "").replace("</ol>", "").replace("<ol>", "")

        with open(f"./stories/{uid}.txt", 'w', encoding="utf-8") as file:
            
            file.write(data_back_title)

            for x in data_back_content:
                file.write(x)


if __name__ == "__main__":
    amount = input("Scrape reddit for how many scrolls (the more scrolls, the more stories): ")
    scrape_reddit(int(amount))