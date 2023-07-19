# -*- coding:utf-8 -*-
# (c) LombardGPT. All Rights Reserved
#  Dileep Jayamal
from selenium.webdriver.chrome.options import Options
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


token = "vLQja2SITLNdYQdphuMBer3423413213nj3n3jrnh3"


class Link(BaseModel):
    url: str
    token: str


app = FastAPI()


@app.post("/get_page/")
async def get_page(link: Link):
    if link.token == token:
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(link.url.strip())
            t = time.time()

            def page_has_loaded():
                page_state = driver.execute_script('return document.readyState;')
                return page_state == 'complete'
            while not page_has_loaded() and time.time()-t < 60:
                time.sleep(0.5)
            if time.time()-t > 60:
                driver.close()
                return ""
            source = driver.page_source
            driver.close()
            return source
        except Exception as ex:
            try:
                driver.close()
            except:
                pass
            return ""
    return "Unauthorized!"


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8890)

