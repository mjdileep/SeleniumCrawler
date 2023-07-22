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
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fastapi.exceptions import HTTPException
from selenium.common.exceptions import TimeoutException


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
    print("Requested page:",link)
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
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            except TimeoutException as ex:
                print("Timeout:")
                print(ex)
            source = driver.page_source
            driver.close()
            return source
        except Exception as ex:
            print("Other:")
            print(ex)
            try:
                driver.close()
            except:
                pass
            return HTTPException(status_code=501, detail="Error occured")
    return HTTPException(status_code=502, detail="Not allowed!")


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8890)

