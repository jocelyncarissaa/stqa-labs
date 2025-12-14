from os import getenv
from selenium import webdriver
import requests

BASE_URL = getenv("BASE_URL", "http://127.0.0.1:5006")

def before_all(context):
    context.base_url = BASE_URL

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    context.driver = webdriver.Chrome(options=options)

    # reset data sebelum test
    requests.post(f"{BASE_URL}/pets/reset")

def after_all(context):
    context.driver.quit()
