import requests
from bs4 import BeautifulSoup

header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
def getResponse(url):
    success = True
    response = requests.get(url, headers=header)
    if (response.status_code != 200):
        print(f"Error got code [{response.status_code}] with url: {url}")
        success = False
    soup = BeautifulSoup(response.text, 'html.parser')
    return [success, soup]
